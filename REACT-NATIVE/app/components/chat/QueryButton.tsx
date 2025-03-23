// components/chat/QueryButton.tsx
import React from 'react';
import { TouchableOpacity, Text } from 'react-native';

interface QueryButtonProps {
  text: string;
  onPress: () => void;
  bgColor: string;
}

const QueryButton: React.FC<QueryButtonProps> = ({ text, onPress, bgColor }) => {
  return (
    <TouchableOpacity
      onPress={onPress}
      className={`bg-[${bgColor}] px-4 py-3 rounded-lg shadow-md`}
    >
      <Text className="text-black">{text}</Text>
    </TouchableOpacity>
  );
};

export default QueryButton;