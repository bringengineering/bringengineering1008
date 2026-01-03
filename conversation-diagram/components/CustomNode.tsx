'use client';

import { Handle, Position } from 'reactflow';
import type { NodeLevel, NodeStatus } from '@/lib/types';

interface CustomNodeProps {
  data: {
    label: string;
    level: NodeLevel;
    status: NodeStatus;
    description?: string;
  };
}

const levelColors = {
  1: 'bg-purple-100 border-purple-500 text-purple-900',
  2: 'bg-blue-100 border-blue-500 text-blue-900',
  3: 'bg-green-100 border-green-500 text-green-900',
  4: 'bg-yellow-100 border-yellow-500 text-yellow-900',
};

const levelLabels = {
  1: 'L1: 목표',
  2: 'L2: 전략',
  3: 'L3: 실행방법',
  4: 'L4: 세부액션',
};

const statusIcons = {
  proposed: '💡',
  decided: '✓',
  active: '🔥',
  deprecated: '⏸',
};

export function CustomNode({ data }: CustomNodeProps) {
  const { label, level, status, description } = data;

  return (
    <div
      className={`px-4 py-3 rounded-lg border-2 shadow-md min-w-[200px] max-w-[280px] ${levelColors[level]}`}
    >
      <Handle type="target" position={Position.Left} />

      <div className="flex items-start justify-between mb-1">
        <span className="text-xs font-semibold opacity-70">{levelLabels[level]}</span>
        <span className="text-sm">{statusIcons[status]}</span>
      </div>

      <div className="font-semibold text-sm mb-1">{label}</div>

      {description && (
        <div className="text-xs opacity-75 mt-2 line-clamp-2">{description}</div>
      )}

      <Handle type="source" position={Position.Right} />
    </div>
  );
}
