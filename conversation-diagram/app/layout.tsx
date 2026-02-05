import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Conversation to Diagram',
  description: '대화를 실시간으로 구조화하는 사고 시각화 엔진',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <body className="antialiased">{children}</body>
    </html>
  );
}
