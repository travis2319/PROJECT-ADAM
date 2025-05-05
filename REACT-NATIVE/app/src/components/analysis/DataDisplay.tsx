import React from 'react';
import { View, Text } from 'react-native';
import { EmissionsData, HealthMonitoringData, PredictiveMaintenanceData } from '../../types/analysis';

export const HealthMonitoringDisplay: React.FC<{ data: HealthMonitoringData | null }> = ({ data }) => {
  if (!data) return null;
  
  return (
    <View>
      <Text className="text-base font-bold mb-2 ml-8 text-black">
        Total Records: {data.summary.total_records}
      </Text>
      <Text className="text-base font-bold mb-2 ml-8 text-black">
        Good Condition: {data.summary.good_condition}
      </Text>
      <Text className="text-base font-bold mb-2 ml-8 text-black">
        Needs Attention: {data.summary.needs_attention}
      </Text>
      <Text className="text-base font-bold mb-2 ml-8 text-black">
        Health Rate: {data.summary.health_rate}%
      </Text>
    </View>
  );
};

export const EmissionsDisplay: React.FC<{ data: EmissionsData | null }> = ({ data }) => {
  if (!data) return null;
  
  return (
    <View>
      <Text className="text-base font-bold mb-2 ml-8 text-black">
        Total Vehicle Values: {data.summary?.total_vehicle_values}
      </Text>
      <Text className="text-base font-bold mb-2 ml-8 text-black">
        Compliant Vehicle Values: {data.summary?.compliant_vehicle_values}
      </Text>
      <Text className="text-base font-bold mb-2 ml-8 text-black">
        Non-Compliant Vehicle Values: {data.summary.non_compliant_vehicle_values}
      </Text>
      <Text className="text-base font-bold mb-2 ml-8 text-black">
        Compliance Rate: {data.summary.compliance_rate}%
      </Text>
      <Text className="text-base font-bold mb-2 ml-8 text-black">
        Start Timestamp: {data.summary.start_timestamp}
      </Text>
      <Text className="text-base font-bold mb-2 ml-8 text-black">
        End Timestamp: {data.summary.end_timestamp}
      </Text>
      <Text className="text-base font-bold mb-2 ml-8 text-black">
        Total Distance Traveled: {data.summary.total_distance_traveled} km
      </Text>
    </View>
  );
};

export const PredictiveMaintenanceDisplay: React.FC<{ data: PredictiveMaintenanceData | null }> = ({ data }) => {
  if (!data) return null;
  
  return (
    <View>
      <Text className="text-base font-bold mb-2 ml-8 text-black">
        Timestamp: {data.summary.timestamp}
      </Text>
      <Text className="text-base font-bold mb-2 ml-8 text-black">
        Total Vehicles: {data.summary.total_vehicles}
      </Text>
      <Text className="text-base font-bold mb-2 ml-8 text-black">
        Critical: {data.summary.status_distribution.Critical}
      </Text>
      <Text className="text-base font-bold mb-2 ml-8 text-black">
        Warning: {data.summary.status_distribution.Warning}
      </Text>
      <Text className="text-base font-bold mb-2 ml-8 text-black">
        Good: {data.summary.status_distribution.Good}
      </Text>
      <Text className="text-base font-bold mb-2 ml-8 text-black">
        Engine: {data.summary.critical_systems.engine}%
      </Text>
      <Text className="text-base font-bold mb-2 ml-8 text-black">
        Coolant: {data.summary.critical_systems.coolant}%
      </Text>
      <Text className="text-base font-bold mb-2 ml-8 text-black">
        Fuel: {data.summary.critical_systems.fuel}%
      </Text>
      <Text className="text-base font-bold mb-2 ml-8 text-black">
        Brake Wear: {data.summary.critical_systems.brake_wear}%
      </Text>
      <Text className="text-base font-bold mb-2 ml-8 text-black">
        Immediate Attention: {data.summary.maintenance_required.immediate_attention}
      </Text>
      <Text className="text-base font-bold mb-2 ml-8 text-black">
        Soon Attention: {data.summary.maintenance_required.soon_attention}
      </Text>
      <Text className="text-base font-bold mb-2 ml-8 text-black">
        Good Condition: {data.summary.maintenance_required.good_condition}
      </Text>
    </View>
  );
};