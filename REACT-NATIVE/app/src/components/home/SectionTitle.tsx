// components/common/SectionTitle.tsx
import React from 'react';
import { Text } from 'react-native';

type SectionTitleProps = {
  title: string;
};

export const SectionTitle: React.FC<SectionTitleProps> = ({ title }) => {
  return (
    <Text className="text-lg font-bold text-[#105e62] mb-3">
      {title}
    </Text>
  );
};