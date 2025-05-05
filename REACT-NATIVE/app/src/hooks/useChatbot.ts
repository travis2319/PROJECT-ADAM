// hooks/useChatbot.ts
import { useState } from 'react';
import { fetchChatbotResponse } from '../services/chatService';
import { USER_ID } from '../constants/chatQuries';

export const useChatbot = () => {
  const [query, setQuery] = useState<string>('');
  const [response, setResponse] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  const handleSendQuery = async () => {
    if (!query) return;

    setLoading(true);
    try {
      const data = await fetchChatbotResponse(query, USER_ID);
      setResponse(data.response || 'No response received.');
    } catch (error) {
      setResponse('Error fetching response. Please try again.');
    } finally {
      setLoading(false);
      setQuery('');
    }
  };

  const handleButtonClick = (buttonText: string) => {
    setQuery(buttonText);
  };

  return {
    query,
    setQuery,
    response,
    loading,
    handleSendQuery,
    handleButtonClick,
  };
};