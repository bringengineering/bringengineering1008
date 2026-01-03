// 핵심 데이터 구조 타입 정의

export type NodeLevel = 1 | 2 | 3 | 4;

export type NodeType = 'goal' | 'strategy' | 'tactic' | 'action';

export type NodeStatus = 'proposed' | 'decided' | 'deprecated' | 'active';

export type OperationType = 'add' | 'update' | 'merge' | 'archive' | 'init';

export interface ConversationNode {
  id: string;
  type: NodeType;
  level: NodeLevel;
  label: string;
  description?: string;
  status: NodeStatus;
  relatedMessages: string[];  // 참조하는 메시지 ID들
  createdAt: string;
  updatedAt: string;
}

export interface ConversationEdge {
  id: string;
  from: string;  // 부모 노드 ID
  to: string;    // 자식 노드 ID
  label?: string;
}

export interface ConversationMetadata {
  projectGoal: string;  // L1: 프로젝트의 핵심 목표
  version: number;
  lastUpdated: string;
  totalMessages: number;
}

export interface ConversationStructure {
  nodes: ConversationNode[];
  edges: ConversationEdge[];
  metadata: ConversationMetadata;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface StructureUpdate {
  operation: OperationType;
  nodes?: ConversationNode[];
  edges?: ConversationEdge[];
  metadata?: Partial<ConversationMetadata>;
  reasoning?: string;  // AI가 왜 이런 구조로 했는지 설명
}

export interface ChatRequest {
  message: string;
  conversationHistory: Message[];
  currentStructure?: ConversationStructure;
}

export interface ChatResponse {
  message: string;
  structureUpdate: StructureUpdate;
  timestamp: string;
}

// React Flow 타입 (렌더링용)
export interface FlowNode {
  id: string;
  type: 'custom';
  data: {
    label: string;
    level: NodeLevel;
    status: NodeStatus;
    description?: string;
  };
  position: { x: number; y: number };
}

export interface FlowEdge {
  id: string;
  source: string;
  target: string;
  type: 'smoothstep';
  animated?: boolean;
}
