// components/home/CarDisplay.tsx
import React from 'react';
import { View, Image } from 'react-native';

type CarDisplayProps = {
  imageUrl: string;
  maxHeight: number;
};

export const CarDisplay: React.FC<CarDisplayProps> = ({ imageUrl, maxHeight }) => {
  return (
    <View className="px-4 -mt-2">
      <Image 
        source={{ uri: imageUrl }}
        className="w-full rounded-3xl shadow-xl"
        style={{ height: maxHeight }}
        resizeMode="cover"
      />
    </View>
  );
};