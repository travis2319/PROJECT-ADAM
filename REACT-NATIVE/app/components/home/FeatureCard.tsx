// components/home/FeatureCard.tsx
import React from 'react';
import { View, Text, Image, TouchableOpacity, ImageSourcePropType } from 'react-native';
import { router } from 'expo-router';

type FeatureCardProps = {
  title: string;
  icon: ImageSourcePropType;
  backgroundColor: string;
  backgroundIcon?: ImageSourcePropType;
  navigateTo?: string;
  cardHeight: number;
};

export const FeatureCard: React.FC<FeatureCardProps> = ({
  title,
  icon,
  backgroundColor,
  backgroundIcon,
  navigateTo,
  cardHeight,
}) => {
  const handlePress = () => {
    if (navigateTo) {
      router.push(navigateTo as any);
    }
  };

  return (
    <TouchableOpacity className="w-1/2 px-1 mb-2" onPress={handlePress}>
      <View 
        className="rounded-xl p-4 justify-between relative"
        style={{ backgroundColor, height: cardHeight }}
      >
        <Text className="text-xl font-bold text-gray-800 z-10">{title}</Text>
        
        <Image source={icon} className="w-10 h-12 self-end z-10" />
        
        {backgroundIcon && (
          <Image
            source={backgroundIcon}
            className="w-40 h-40 absolute -left-2 -top-1 opacity-30 z-0"
          />
        )}
      </View>
    </TouchableOpacity>
  );
};