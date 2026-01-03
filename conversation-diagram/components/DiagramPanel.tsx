'use client';

import { useEffect, useMemo } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { useConversationStore } from '@/store/conversation-store';
import { structureToFlowNodes } from '@/lib/structure-extractor';
import { CustomNode } from './CustomNode';

const nodeTypes = {
  custom: CustomNode,
};

export function DiagramPanel() {
  const structure = useConversationStore((state) => state.structure);
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  useEffect(() => {
    if (structure) {
      const { nodes: flowNodes, edges: flowEdges } = structureToFlowNodes(structure);
      setNodes(flowNodes);
      setEdges(flowEdges);
    }
  }, [structure, setNodes, setEdges]);

  const isEmpty = nodes.length === 0;

  return (
    <div className="h-full bg-gray-50 relative">
      {isEmpty ? (
        <div className="absolute inset-0 flex items-center justify-center text-gray-400">
          <div className="text-center">
            <div className="text-6xl mb-4">🗺️</div>
            <h3 className="text-lg font-semibold mb-2">대화를 시작하세요</h3>
            <p className="text-sm">
              AI와 대화하면 실시간으로 구조가 여기에 나타납니다
            </p>
          </div>
        </div>
      ) : (
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          nodeTypes={nodeTypes}
          fitView
          attributionPosition="bottom-left"
        >
          <Background />
          <Controls />
          <MiniMap
            nodeColor={(node) => {
              const level = node.data.level;
              const colors = {
                1: '#9333ea',
                2: '#3b82f6',
                3: '#22c55e',
                4: '#eab308',
              };
              return colors[level as 1 | 2 | 3 | 4] || '#gray';
            }}
          />
        </ReactFlow>
      )}
    </div>
  );
}
