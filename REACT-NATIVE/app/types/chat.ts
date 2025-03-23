// types/chat.ts
export interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'bot';
  timestamp: string;
}

export interface QuickAction {
  label: string;
  bgColor: string;
}

export interface ChatResponse {
  response: string;
}