// hooks/useChat.ts
import { useState } from 'react';
import { Alert } from 'react-native';
import { fetchChatResponse } from '../services/chatService';
import { useAuth } from '@/utils/auth'; // Assuming you have an auth context

export const useChat = () => {
  const [query, setQuery] = useState<string>('');
  const [response, setResponse] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const { user } = useAuth(); // Get user from auth context
  
  const handleSendQuery = async () => {
    if (!query) return;
    
    setLoading(true);
    try {
      const data = await fetchChatResponse(query, user?.id || 'anonymous');
      setResponse(data.response || 'No response received.');
      setQuery(''); // Clear input after sending
    } catch (error) {
      console.error('Error in chat:', error);
      Alert.alert(
        'Error',
        'Failed to get response from the server. Please check your connection and try again.'
      );
      setResponse('Error fetching response. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  const setPresetQuery = (buttonText: string) => {
    setQuery(buttonText);
  };
  
  return {
    query,
    setQuery,
    response,
    loading,
    handleSendQuery,
    setPresetQuery
  };
};