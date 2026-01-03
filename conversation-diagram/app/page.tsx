'use client';

import { ChatPanel } from '@/components/ChatPanel';
import { DiagramPanel } from '@/components/DiagramPanel';
import { useConversationStore } from '@/store/conversation-store';

export default function Home() {
  const clearConversation = useConversationStore((state) => state.clearConversation);
  const exportAsMarkdown = useConversationStore((state) => state.exportAsMarkdown);
  const structure = useConversationStore((state) => state.structure);

  const handleExportMarkdown = () => {
    const markdown = exportAsMarkdown();
    const blob = new Blob([markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `conversation-structure-${Date.now()}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleClear = () => {
    if (confirm('모든 대화와 구조를 초기화하시겠습니까?')) {
      clearConversation();
    }
  };

  return (
    <div className="h-screen flex flex-col">
      {/* 헤더 */}
      <header className="h-16 border-b bg-white shadow-sm flex items-center justify-between px-6">
        <div className="flex items-center space-x-3">
          <h1 className="text-xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
            Conversation to Diagram
          </h1>
          <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded">
            MVP
          </span>
        </div>

        <div className="flex items-center space-x-2">
          {structure && (
            <>
              <button
                onClick={handleExportMarkdown}
                className="px-4 py-2 text-sm bg-green-500 text-white rounded hover:bg-green-600 transition-colors"
              >
                📄 Export MD
              </button>
              <button
                onClick={handleClear}
                className="px-4 py-2 text-sm bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
              >
                🗑️ Clear
              </button>
            </>
          )}
        </div>
      </header>

      {/* 메인 컨텐츠: 좌우 분할 */}
      <div className="flex-1 flex overflow-hidden">
        {/* 왼쪽: 채팅 */}
        <div className="w-1/2 border-r">
          <ChatPanel />
        </div>

        {/* 오른쪽: 도식화 */}
        <div className="w-1/2">
          <DiagramPanel />
        </div>
      </div>

      {/* 푸터 (상태 표시) */}
      {structure && (
        <footer className="h-10 border-t bg-gray-50 flex items-center justify-between px-6 text-xs text-gray-600">
          <div className="flex items-center space-x-4">
            <span>
              📊 Nodes: <strong>{structure.nodes.length}</strong>
            </span>
            <span>
              🔗 Edges: <strong>{structure.edges.length}</strong>
            </span>
            <span>
              v{structure.metadata.version}
            </span>
          </div>
          <div>
            {structure.metadata.projectGoal && (
              <span className="italic">
                "{structure.metadata.projectGoal}"
              </span>
            )}
          </div>
        </footer>
      )}
    </div>
  );
}
