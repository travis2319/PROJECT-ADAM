// components/home/MetricsRow.tsx
import React from 'react';
import { View } from 'react-native';
import { MetricCard } from './MetricCard';

// Import images
import rpm from "@/assets/images/rpm.png";
import rpm2 from "@/assets/images/rpm2.png";
import speed from "@/assets/images/speed.png";
import speed2 from "@/assets/images/speed2.png";

type MetricData = {
  value: number;
  unit: string;
};

type MetricsRowProps = {
  rpm: MetricData;
  speed: MetricData;
};

export const MetricsRow: React.FC<MetricsRowProps> = ({ rpm: rpmData, speed: speedData }) => {
  return (
    <View className="flex-row mt-6 px-4">
      <MetricCard
        title="RPM"
        value={rpmData.value}
        unit={rpmData.unit}
        icon={rpm}
        backgroundIcon={rpm2}
        backgroundColor="#ffab76"
        className="mr-2"
      />
      
      <MetricCard
        title="Speed"
        value={speedData.value}
        unit={speedData.unit}
        icon={speed}
        backgroundIcon={speed2}
        backgroundColor="#93c6e7"
        className="ml-2"
      />
    </View>
  );
};