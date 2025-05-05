// components/chat/ChatInput.tsx
import React from 'react';
import { 
  View, 
  TextInput, 
  TouchableOpacity, 
  ActivityIndicator, 
  KeyboardAvoidingView, 
  Platform 
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface ChatInputProps {
  query: string;
  setQuery: (text: string) => void;
  loading: boolean;
  onSend: () => void;
}

const ChatInput: React.FC<ChatInputProps> = ({ 
  query, 
  setQuery, 
  loading, 
  onSend 
}) => {
  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={{ marginBottom: 90 }}
    >
      <View className="bg-[#e6dfd3] flex-row items-center px-4 py-3 rounded-lg shadow-md">
        <TextInput
          placeholder="Ask Query"
          placeholderTextColor="#000"
          className="flex-1 text-black"
          style={{ height: 40 }}
          value={query}
          onChangeText={setQuery}
        />
        <TouchableOpacity onPress={onSend} disabled={loading}>
          {loading ? (
            <ActivityIndicator size="small" color="#5a503d" />
          ) : (
            <Ionicons name="search" size={30} color="#5a503d" />
          )}
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
};

export default ChatInput;