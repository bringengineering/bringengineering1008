import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type {
  Message,
  ConversationStructure,
  ConversationNode,
  ConversationEdge,
  StructureUpdate,
} from '@/lib/types';

interface ConversationState {
  // 대화 상태
  messages: Message[];
  isLoading: boolean;

  // 구조 상태
  structure: ConversationStructure | null;

  // Actions
  addMessage: (message: Message) => void;
  setLoading: (loading: boolean) => void;
  updateStructure: (update: StructureUpdate) => void;
  clearConversation: () => void;

  // Export
  exportAsMarkdown: () => string;
  exportAsJSON: () => string;
}

const initialStructure: ConversationStructure = {
  nodes: [],
  edges: [],
  metadata: {
    projectGoal: '',
    version: 1,
    lastUpdated: new Date().toISOString(),
    totalMessages: 0,
  },
};

export const useConversationStore = create<ConversationState>()(
  persist(
    (set, get) => ({
      messages: [],
      isLoading: false,
      structure: null,

      addMessage: (message) => {
        set((state) => ({
          messages: [...state.messages, message],
          structure: state.structure
            ? {
                ...state.structure,
                metadata: {
                  ...state.structure.metadata,
                  totalMessages: state.structure.metadata.totalMessages + 1,
                },
              }
            : null,
        }));
      },

      setLoading: (loading) => set({ isLoading: loading }),

      updateStructure: (update) => {
        set((state) => {
          const currentStructure = state.structure || initialStructure;

          let newNodes = [...currentStructure.nodes];
          let newEdges = [...currentStructure.edges];
          let newMetadata = { ...currentStructure.metadata };

          switch (update.operation) {
            case 'init':
            case 'add':
              if (update.nodes) {
                // 새 노드 추가 (중복 체크)
                update.nodes.forEach((node) => {
                  const existingIndex = newNodes.findIndex((n) => n.id === node.id);
                  if (existingIndex >= 0) {
                    newNodes[existingIndex] = node;
                  } else {
                    newNodes.push(node);
                  }
                });
              }
              if (update.edges) {
                // 새 엣지 추가
                update.edges.forEach((edge) => {
                  const existingIndex = newEdges.findIndex((e) => e.id === edge.id);
                  if (existingIndex >= 0) {
                    newEdges[existingIndex] = edge;
                  } else {
                    newEdges.push(edge);
                  }
                });
              }
              break;

            case 'update':
              if (update.nodes) {
                update.nodes.forEach((node) => {
                  const index = newNodes.findIndex((n) => n.id === node.id);
                  if (index >= 0) {
                    newNodes[index] = { ...newNodes[index], ...node };
                  }
                });
              }
              break;

            case 'archive':
              if (update.nodes) {
                update.nodes.forEach((node) => {
                  const index = newNodes.findIndex((n) => n.id === node.id);
                  if (index >= 0) {
                    newNodes[index] = { ...newNodes[index], status: 'deprecated' };
                  }
                });
              }
              break;

            case 'merge':
              // TODO: 노드 병합 로직 구현
              break;
          }

          if (update.metadata) {
            newMetadata = { ...newMetadata, ...update.metadata };
          }

          newMetadata.lastUpdated = new Date().toISOString();
          newMetadata.version += 1;

          return {
            structure: {
              nodes: newNodes,
              edges: newEdges,
              metadata: newMetadata,
            },
          };
        });
      },

      clearConversation: () => {
        set({
          messages: [],
          structure: null,
        });
      },

      exportAsMarkdown: () => {
        const { structure, messages } = get();
        if (!structure) return '# No structure yet';

        const lines: string[] = [];
        lines.push(`# ${structure.metadata.projectGoal || 'Project Structure'}`);
        lines.push('');
        lines.push(`*Last updated: ${new Date(structure.metadata.lastUpdated).toLocaleString()}*`);
        lines.push(`*Version: ${structure.metadata.version}*`);
        lines.push('');

        // L1 노드부터 계층적으로 출력
        const renderNode = (node: ConversationNode, indent: number = 0) => {
          const prefix = '  '.repeat(indent) + '-';
          const status = node.status !== 'decided' ? ` [${node.status}]` : '';
          lines.push(`${prefix} **${node.label}**${status}`);
          if (node.description) {
            lines.push(`${'  '.repeat(indent + 1)}*${node.description}*`);
          }

          // 자식 노드 찾기
          const childEdges = structure.edges.filter((e) => e.from === node.id);
          childEdges.forEach((edge) => {
            const childNode = structure.nodes.find((n) => n.id === edge.to);
            if (childNode) {
              renderNode(childNode, indent + 1);
            }
          });
        };

        const rootNodes = structure.nodes.filter((n) => n.level === 1);
        rootNodes.forEach((node) => renderNode(node));

        return lines.join('\n');
      },

      exportAsJSON: () => {
        const { structure } = get();
        return JSON.stringify(structure, null, 2);
      },
    }),
    {
      name: 'conversation-storage',
    }
  )
);
