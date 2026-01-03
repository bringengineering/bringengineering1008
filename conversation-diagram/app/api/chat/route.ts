import { NextRequest, NextResponse } from 'next/server';
import Anthropic from '@anthropic-ai/sdk';
import { extractStructure } from '@/lib/structure-extractor';
import type { ChatRequest, Message } from '@/lib/types';

export const runtime = 'edge';

export async function POST(req: NextRequest) {
  try {
    const { message, conversationHistory, currentStructure }: ChatRequest = await req.json();

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) {
      return NextResponse.json(
        { error: 'ANTHROPIC_API_KEY not configured' },
        { status: 500 }
      );
    }

    const anthropic = new Anthropic({ apiKey });

    // 1. AI 응답 생성
    const messagesForClaude = conversationHistory.map((m) => ({
      role: m.role,
      content: m.content,
    }));

    messagesForClaude.push({
      role: 'user',
      content: message,
    });

    const response = await anthropic.messages.create({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 2048,
      temperature: 0.7,
      system: `You are a helpful assistant for a thought visualization system.

Have natural conversations with the user about their project ideas, challenges, and plans.
Ask clarifying questions when needed. Help them refine their thinking.

Remember: Your responses will be analyzed to extract project structure automatically,
so try to discuss things in a structured way when appropriate.`,
      messages: messagesForClaude as Anthropic.MessageParam[],
    });

    const assistantMessage = response.content[0];
    if (assistantMessage.type !== 'text') {
      throw new Error('Unexpected response type');
    }

    // 2. 대화 히스토리 업데이트
    const userMsg: Message = {
      id: `msg-${Date.now()}-user`,
      role: 'user',
      content: message,
      timestamp: new Date().toISOString(),
    };

    const assistantMsg: Message = {
      id: `msg-${Date.now()}-assistant`,
      role: 'assistant',
      content: assistantMessage.text,
      timestamp: new Date().toISOString(),
    };

    const updatedHistory = [...conversationHistory, userMsg, assistantMsg];

    // 3. 구조 추출
    const structureUpdate = await extractStructure(
      updatedHistory,
      currentStructure || null,
      apiKey
    );

    return NextResponse.json({
      message: assistantMessage.text,
      structureUpdate,
      timestamp: new Date().toISOString(),
      userMessage: userMsg,
      assistantMessage: assistantMsg,
    });
  } catch (error: any) {
    console.error('Chat API error:', error);
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500 }
    );
  }
}
