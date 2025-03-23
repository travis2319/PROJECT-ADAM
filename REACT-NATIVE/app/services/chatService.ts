// services/chatService.ts
import { Alert } from 'react-native';

const BASE_URL = 'http://192.168.242.63:8000';
const USERNAME = 'user';
const PASSWORD = 'password';

export interface ChatResponse {
  response: string;
  // Add other response fields if needed
}

export const fetchChatbotResponse = async (
  query: string,
  userId: string
): Promise<ChatResponse> => {
  const currentTime = new Date().toISOString();
  
  try {
    const encodedQuery = encodeURIComponent(query);
    const url = `${BASE_URL}/chatbot/ask?query=${encodedQuery}&user_id=${userId}&current_time=${currentTime}`;
    
    const encodedCredentials = btoa(`${USERNAME}:${PASSWORD}`);
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'accept': 'application/json',
        'Authorization': `Basic ${encodedCredentials}`,
      },
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('Chatbot Response:', data);
    return data;
    
  } catch (error) {
    console.error('Error fetching chatbot response:', error);
    Alert.alert(
      'Error',
      'Failed to get response from the server. Please check your connection and try again.'
    );
    throw error;
  }
};