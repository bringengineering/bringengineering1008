import Anthropic from '@anthropic-ai/sdk';
import type {
  Message,
  ConversationStructure,
  StructureUpdate,
  ConversationNode,
} from './types';

const STRUCTURE_EXTRACTION_PROMPT = `You are a conversation structure analyzer for a thought visualization system.

Your task is to analyze conversations and extract hierarchical structure in 4 levels:

**L1 (Goal)**: Project goal, problem definition, core value proposition
  - Should be stable and rarely change
  - If changing L1, mark it clearly

**L2 (Strategy)**: Strategic approaches - technology, business, constraints
  - Major decisions and directions

**L3 (Tactic)**: Tactical implementations and specific methods
  - How to execute the strategies

**L4 (Action)**: Concrete actions, features, tasks
  - Specific things to do or build

**Rules:**
1. L1 should stabilize quickly and not change unless the project pivots
2. When refining existing ideas, UPDATE nodes rather than creating duplicates
3. When a concept is abandoned, mark status as "deprecated"
4. Keep labels concise (3-8 words)
5. Add descriptions for context when needed

**Output Format:**
You MUST respond with valid JSON matching this schema:

{
  "operation": "init" | "add" | "update" | "archive",
  "nodes": [
    {
      "id": "unique-id",
      "type": "goal" | "strategy" | "tactic" | "action",
      "level": 1 | 2 | 3 | 4,
      "label": "Short label",
      "description": "Optional longer explanation",
      "status": "proposed" | "decided" | "active" | "deprecated",
      "relatedMessages": ["msg-id"],
      "createdAt": "ISO date",
      "updatedAt": "ISO date"
    }
  ],
  "edges": [
    {
      "id": "edge-id",
      "from": "parent-node-id",
      "to": "child-node-id"
    }
  ],
  "metadata": {
    "projectGoal": "One sentence project goal",
    "version": 1,
    "lastUpdated": "ISO date",
    "totalMessages": 1
  },
  "reasoning": "Brief explanation of what changed and why"
}

**Important:**
- For first message: use operation "init"
- For updates: use operation "add" or "update"
- Always include reasoning
- Node IDs should be stable (use slugified labels)
- Respect existing structure when provided`;

export async function extractStructure(
  messages: Message[],
  currentStructure: ConversationStructure | null,
  apiKey: string
): Promise<StructureUpdate> {
  const anthropic = new Anthropic({
    apiKey,
  });

  // 최근 메시지 (마지막 사용자 메시지)
  const latestMessage = messages[messages.length - 1];
  const conversationContext = messages
    .slice(-10) // 최근 10개 메시지만 컨텍스트로
    .map((m) => `${m.role}: ${m.content}`)
    .join('\n\n');

  const userPrompt = `
Current conversation:
${conversationContext}

${
  currentStructure
    ? `
Current structure:
${JSON.stringify(currentStructure, null, 2)}
`
    : 'This is the first message. Initialize the structure.'
}

Latest user message: "${latestMessage.content}"

Analyze this conversation and update the structure accordingly. Output JSON only.`;

  try {
    const response = await anthropic.messages.create({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 4096,
      temperature: 0.3,
      system: STRUCTURE_EXTRACTION_PROMPT,
      messages: [
        {
          role: 'user',
          content: userPrompt,
        },
      ],
    });

    const content = response.content[0];
    if (content.type !== 'text') {
      throw new Error('Unexpected response type');
    }

    // JSON 파싱
    const jsonMatch = content.text.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error('No JSON found in response');
    }

    const structureUpdate: StructureUpdate = JSON.parse(jsonMatch[0]);

    // ID와 타임스탬프 보강
    if (structureUpdate.nodes) {
      structureUpdate.nodes = structureUpdate.nodes.map((node) => ({
        ...node,
        id: node.id || generateNodeId(node.label),
        createdAt: node.createdAt || new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        relatedMessages: [latestMessage.id],
      }));
    }

    if (structureUpdate.edges) {
      structureUpdate.edges = structureUpdate.edges.map((edge) => ({
        ...edge,
        id: edge.id || `${edge.from}-to-${edge.to}`,
      }));
    }

    return structureUpdate;
  } catch (error) {
    console.error('Structure extraction error:', error);
    throw error;
  }
}

function generateNodeId(label: string): string {
  return label
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/\s+/g, '-')
    .substring(0, 50) +
    '-' +
    Math.random().toString(36).substring(2, 9);
}

// 구조를 React Flow 노드로 변환
export function structureToFlowNodes(structure: ConversationStructure) {
  const nodes = structure.nodes.map((node, index) => {
    // 레벨에 따라 x 위치 결정
    const x = (node.level - 1) * 300;

    // y 위치는 같은 레벨 내에서 순서대로
    const sameLevel = structure.nodes.filter((n) => n.level === node.level);
    const indexInLevel = sameLevel.indexOf(node);
    const y = indexInLevel * 120;

    return {
      id: node.id,
      type: 'custom',
      data: {
        label: node.label,
        level: node.level,
        status: node.status,
        description: node.description,
      },
      position: { x, y },
    };
  });

  const edges = structure.edges.map((edge) => ({
    id: edge.id,
    source: edge.from,
    target: edge.to,
    type: 'smoothstep' as const,
    animated: false,
  }));

  return { nodes, edges };
}
