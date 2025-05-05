// components/home/MetricCard.tsx
import React from 'react';
import { View, Text, Image, ImageSourcePropType } from 'react-native';

type MetricCardProps = {
  title: string;
  value: number;
  unit: string;
  icon: ImageSourcePropType;
  backgroundIcon: ImageSourcePropType;
  backgroundColor: string;
  className?: string;
};

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  unit,
  icon,
  backgroundIcon,
  backgroundColor,
  className = "",
}) => {
  return (
    <View 
      className={`flex-1 p-4 rounded-xl relative ${className}`}
      style={{ backgroundColor }}
    >
      <View className="flex-row items-center">
        <Image
          source={icon}
          className="w-9 h-7 mr-2 text-white"
        />
        <Text className="text-base text-white font-bold">{title}</Text>
      </View>
      <View className="flex-row items-baseline mt-2">
        <Text className="text-2xl font-bold text-gray-800">{value}</Text>
        <Text className="text-xs text-gray-600 ml-1 z-10">{unit}</Text>
      </View>
      <Image
        source={backgroundIcon}
        className="w-28 h-24 absolute -right-5 -bottom-2.5 text-white opacity-50 z-0"
      />
    </View>
  );
};