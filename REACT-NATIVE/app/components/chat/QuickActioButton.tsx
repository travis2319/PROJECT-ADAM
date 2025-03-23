// components/chat/QuickActionButton.tsx
import React from 'react';
import { TouchableOpacity, Text } from 'react-native';

interface QuickActionButtonProps {
  label: string;
  bgColor: string;
  onPress: (text: string) => void;
}

const QuickActionButton: React.FC<QuickActionButtonProps> = ({ 
  label, 
  bgColor, 
  onPress 
}) => {
  return (
    <TouchableOpacity
      onPress={() => onPress(label)}
      className={`px-4 py-3 rounded-lg shadow-md`}
      style={{ backgroundColor: bgColor }}
    >
      <Text className="text-black">{label}</Text>
    </TouchableOpacity>
  );
};

export default QuickActionButton;