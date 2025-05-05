import React from 'react';
import { View, Text, TouchableOpacity, ActivityIndicator } from 'react-native';
import { FontAwesome6 } from '@expo/vector-icons';

interface DataCardProps {
  title: string;
  icon: React.ReactNode;
  bgColor: string;
  iconBgColor: string;
  loading: boolean;
  disabled: boolean;
  onFetch: () => void;
  children: React.ReactNode;
}

const DataCard: React.FC<DataCardProps> = ({
  title,
  icon,
  bgColor,
  iconBgColor,
  loading,
  disabled,
  onFetch,
  children,
}) => {
  return (
    <View className={`bg-[${bgColor}] rounded-2xl shadow-md p-7 relative`}>
      <View className={`absolute -top-4 -left-4 bg-[${iconBgColor}] rounded-full p-4 shadow-md`}>
        {icon}
      </View>
      <Text className="text-base font-bold mb-16 ml-8 text-black">
        {title}
      </Text>
      
      {loading ? (
        <ActivityIndicator size="large" color="#0000ff" />
      ) : (
        children
      )}
      
      <TouchableOpacity 
        className={`self-end bg-[${iconBgColor}] rounded-full p-3 ${disabled ? 'opacity-50' : ''}`} 
        onPress={onFetch}
        disabled={disabled}
      >
        <FontAwesome6 name="searchengin" size={26} color="#000000" />
      </TouchableOpacity>
    </View>
  );
};

export default DataCard;