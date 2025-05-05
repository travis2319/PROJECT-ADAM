// constants/chatQuries.ts
import { QuickAction } from '../types/chat';

// Add this to your existing chatQuries.ts file

export const USER_ID = 'VOID-001';

export const QUICK_ACTIONS: QuickAction[][] = [
  [
    { label: 'Spark Plug Replacement', bgColor: '#eee5db' },
    { label: 'Air Filter Replacement', bgColor: '#eee5db' },
  ],
  [
    { label: 'Battery Health', bgColor: '#faf4ce' },
    { label: 'Coolant Change', bgColor: '#faf4ce' },
  ],
  [
    { label: 'Estimate Oil Change', bgColor: '#f4d7c3' },
    { label: 'Estimate Brake Pad Wear', bgColor: '#f4d7c3' },
  ],
];