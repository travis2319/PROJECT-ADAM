// components/home/FeatureGrid.tsx
import React from 'react';
import { View } from 'react-native';
import { FeatureCard } from './FeatureCard';
import { FeatureType } from '@/types/features';

type FeatureGridProps = {
  features: FeatureType[];
  cardHeight: number;
};

export const FeatureGrid: React.FC<FeatureGridProps> = ({ features, cardHeight }) => {
  return (
    <View className="flex-row flex-wrap px-3">
      {features.map((feature, index) => (
        <FeatureCard
          key={index}
          title={feature.title}
          icon={feature.icon}
          backgroundIcon={feature.backgroundIcon}
          backgroundColor={feature.backgroundColor}
          navigateTo={feature.navigateTo}
          cardHeight={cardHeight}
        />
      ))}
    </View>
  );
};