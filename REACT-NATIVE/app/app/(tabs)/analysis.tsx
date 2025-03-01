import { View, Text, TouchableOpacity, ScrollView, ActivityIndicator } from 'react-native'
import React, { useState } from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'
import axios from 'axios'
import { MaterialCommunityIcons, FontAwesome5, FontAwesome6, FontAwesome } from '@expo/vector-icons'
import cardData from '../../constants/cardData'

const Analysis = () => {
  interface EmissionsData {
    summary: {
      total_vehicle_values: number;
      compliant_vehicle_values: number;
      non_compliant_vehicle_values: number;
      compliance_rate: number;
      start_timestamp: string;
      end_timestamp: string;
      total_distance_traveled: number;
      total_records: number;
      good_condition: number;
      needs_attention: number;
      health_rate: number;
    };
  }
  
  const [emissionsData, setEmissionsData] = useState<EmissionsData | null>(null);
  const [loadingEmissions, setLoadingEmissions] = useState(false);
  const [loadingHealthMonitoring, setLoadingHealthMonitoring] = useState(false);
  const [loadingPredictiveMaintenance, setLoadingPredictiveMaintenance] = useState(false);

  const [healthMonitoringDisabled, setHealthMonitoringDisabled] = useState(false);
  const [emissionsDisabled, setEmissionsDisabled] = useState(false);
  const [predictiveMaintenanceDisabled, setPredictiveMaintenanceDisabled] = useState(false);

  interface HealthMonitoringData {
    summary: {
      total_vehicle_values: number;
      compliant_vehicle_values: number;
      non_compliant_vehicle_values: number;
      compliance_rate: number;
      start_timestamp: string;
      end_timestamp: string;
      total_distance_traveled: number;
    };
  }

  const [healthMonitoringData, setHealthMonitoringData] = useState<HealthMonitoringData | null>(null);
  interface PredictiveMaintenanceData {
    summary: {
      timestamp: string;
      total_vehicles: number;
      status_distribution: {
        Critical: number;
        Warning: number;
        Good: number;
      };
      critical_systems: {
        engine: number;
        coolant: number;
        fuel: number;
        brake_wear: number;
      };
      maintenance_required: {
        immediate_attention: number;
        soon_attention: number;
        good_condition: number;
      };
    };
  }
  
  const [predictiveMaintenanceData, setPredictiveMaintenanceData] = useState<PredictiveMaintenanceData | null>(null);

  const baseURL = 'http://192.168.251.63:8000';

  const fetchEmissionsData = async () => {
    setLoadingEmissions(true);
    setEmissionsDisabled(true);
    try {
      const response = await axios.get(`${baseURL}/emissions/compliance-and-plot-data`, {
        auth: {
          username: 'user',
          password: 'password'
        }
      });
      setEmissionsData(response.data);
      console.log(JSON.stringify(response.data, null, 2));
    } catch (error) {
      console.error('Fetch error:', error);
    } finally {
      setLoadingEmissions(false);
      setEmissionsDisabled(false);
    }
  };

  const fetchHealthMonitoringData = async () => {
    setLoadingHealthMonitoring(true);
    setHealthMonitoringDisabled(true);
    try {
      const response = await axios.get(`${baseURL}/engine-health/diagnose`, {
        auth: {
          username: 'user',
          password: 'password'
        }
      });
      setHealthMonitoringData(response.data);
      console.log(JSON.stringify(response.data, null, 2));
    } catch (error) {
      console.error('Fetch error:', error);
    } finally {
      setLoadingHealthMonitoring(false);
      setHealthMonitoringDisabled(false);
    }
  };
  
  const fetchPredictiveMaintenanceData = async () => {
    setLoadingPredictiveMaintenance(true);
    setPredictiveMaintenanceDisabled(true);
    try {
      const response = await axios.get(`${baseURL}/predictive-maintenance/diagnose`, {
        auth: {
          username: 'user',
          password: 'password'
        }
      });
      setPredictiveMaintenanceData(response.data);
      console.log(JSON.stringify(response.data, null, 2));
    } catch (error) {
      console.error('Fetch error:', error);
    } finally {
      setLoadingPredictiveMaintenance(false);
      setPredictiveMaintenanceDisabled(false);
    }
  };
  return (
    <SafeAreaView className="flex-1 bg-[#f1f4de]">
      <ScrollView>
        <View className='flex-1 p-12 bg-[#f1f4de] gap-6'>
        
          <View  className={`bg-[#C4E3FA] rounded-2xl shadow-md p-7 relative`}>
            <View className={`absolute -top-4 -left-4 bg-[#54B0E3] rounded-full p-4 shadow-md`}>                
                <MaterialCommunityIcons name='engine' size={32} color="#000000" />
            </View>
            <Text className="text-base font-bold mb-16 ml-8 text-black">
            Engine Health Monitoring
            </Text>
            {loadingHealthMonitoring ? (
              <ActivityIndicator size="large" color="#0000ff" />
            ) : (
              healthMonitoringData && (
                <View>
                  <Text className="text-base font-bold mb-2 ml-8 text-black">
                    Total Records: {healthMonitoringData.summary.total_records}
                  </Text>
                  <Text className="text-base font-bold mb-2 ml-8 text-black">
                    Good Condition: {healthMonitoringData.summary.good_condition}
                  </Text>
                  <Text className="text-base font-bold mb-2 ml-8 text-black">
                    Needs Attention: {healthMonitoringData.summary.needs_attention}
                  </Text>
                  <Text className="text-base font-bold mb-2 ml-8 text-black">
                    Health Rate: {healthMonitoringData.summary.health_rate}%
                  </Text>
                </View>
              )
            )}
            <TouchableOpacity 
              className={`self-end bg-[#54B0E3] rounded-full p-3 ${healthMonitoringDisabled ? 'opacity-50' : ''}`} 
              onPress={fetchHealthMonitoringData}
              disabled={healthMonitoringDisabled}
            >
              <FontAwesome6 name="searchengin" size={26} color="#000000" />
            </TouchableOpacity>
          </View>

          <View  className={`bg-[#A8E7E3] rounded-2xl shadow-md p-7 relative`}>
            <View className={`absolute -top-4 -left-4 bg-[#39C1C5] rounded-full p-4 shadow-md`}>                
                <FontAwesome5 name='shipping-fast' size={32} color="#000000" />
            </View>
            <Text className="text-base font-bold mb-16 ml-8 text-black">
            Emission Compliance
            </Text>
            {loadingEmissions ? (
              <ActivityIndicator size="large" color="#0000ff" />
            ) : (
              emissionsData && (
                <View>
                  <Text className="text-base font-bold mb-2 ml-8 text-black">
                    Total Vehicle Values: {emissionsData.summary?.total_vehicle_values}
                  </Text>
                  <Text className="text-base font-bold mb-2 ml-8 text-black">
                    Compliant Vehicle Values: {emissionsData.summary?.compliant_vehicle_values}
                  </Text>
                  <Text className="text-base font-bold mb-2 ml-8 text-black">
                    Non-Compliant Vehicle Values: {emissionsData.summary.non_compliant_vehicle_values}
                  </Text>
                  <Text className="text-base font-bold mb-2 ml-8 text-black">
                    Compliance Rate: {emissionsData.summary.compliance_rate}%
                  </Text>
                  <Text className="text-base font-bold mb-2 ml-8 text-black">
                    Start Timestamp: {emissionsData.summary.start_timestamp}
                  </Text>
                  <Text className="text-base font-bold mb-2 ml-8 text-black">
                    End Timestamp: {emissionsData.summary.end_timestamp}
                  </Text>
                  <Text className="text-base font-bold mb-2 ml-8 text-black">
                    Total Distance Traveled: {emissionsData.summary.total_distance_traveled} km
                  </Text>
                </View>
              )
            )}
            <TouchableOpacity 
              className={`self-end bg-[#39C1C5] rounded-full p-3 ${emissionsDisabled ? 'opacity-50' : ''}`} 
              onPress={fetchEmissionsData}
              disabled={emissionsDisabled}
            >
              <FontAwesome6 name="searchengin" size={26} color="#000000" />
            </TouchableOpacity>
          </View>

          <View  className={`bg-[#EEE79D] rounded-2xl shadow-md p-7 relative`}>
            <View className={`absolute -top-4 -left-4 bg-[#DAC912] rounded-full p-4 shadow-md`}>                
                <FontAwesome5 name='tools' size={32} color="#000000" />
            </View>
            <Text className="text-base font-bold mb-16 ml-8 text-black">
            Predictive Maintenance
            </Text>
            {loadingPredictiveMaintenance ? (
              <ActivityIndicator size="large" color="#0000ff" />
            ) : (
              predictiveMaintenanceData && (
                <View>
                  <Text className="text-base font-bold mb-2 ml-8 text-black">
                    Timestamp: {predictiveMaintenanceData.summary.timestamp}
                  </Text>
                  <Text className="text-base font-bold mb-2 ml-8 text-black">
                    Total Vehicles: {predictiveMaintenanceData.summary.total_vehicles}
                  </Text>
                  <Text className="text-base font-bold mb-2 ml-8 text-black">
                    Critical: {predictiveMaintenanceData.summary.status_distribution.Critical}
                  </Text>
                  <Text className="text-base font-bold mb-2 ml-8 text-black">
                    Warning: {predictiveMaintenanceData.summary.status_distribution.Warning}
                  </Text>
                  <Text className="text-base font-bold mb-2 ml-8 text-black">
                    Good: {predictiveMaintenanceData.summary.status_distribution.Good}
                  </Text>
                  <Text className="text-base font-bold mb-2 ml-8 text-black">
                    Engine: {predictiveMaintenanceData.summary.critical_systems.engine}%
                  </Text>
                  <Text className="text-base font-bold mb-2 ml-8 text-black">
                    Coolant: {predictiveMaintenanceData.summary.critical_systems.coolant}%
                  </Text>
                  <Text className="text-base font-bold mb-2 ml-8 text-black">
                    Fuel: {predictiveMaintenanceData.summary.critical_systems.fuel}%
                  </Text>
                  <Text className="text-base font-bold mb-2 ml-8 text-black">
                    Brake Wear: {predictiveMaintenanceData.summary.critical_systems.brake_wear}%
                  </Text>
                  <Text className="text-base font-bold mb-2 ml-8 text-black">
                    Immediate Attention: {predictiveMaintenanceData.summary.maintenance_required.immediate_attention}
                  </Text>
                  <Text className="text-base font-bold mb-2 ml-8 text-black">
                    Soon Attention: {predictiveMaintenanceData.summary.maintenance_required.soon_attention}
                  </Text>
                  <Text className="text-base font-bold mb-2 ml-8 text-black">
                    Good Condition: {predictiveMaintenanceData.summary.maintenance_required.good_condition}
                  </Text>
                </View>
              )
            )}
            <TouchableOpacity 
              className={`self-end bg-[#DAC912] rounded-full p-3 ${predictiveMaintenanceDisabled ? 'opacity-50' : ''}`} 
              onPress={fetchPredictiveMaintenanceData}
              disabled={predictiveMaintenanceDisabled}
            >
              <FontAwesome6 name="searchengin" size={26} color="#000000" />
            </TouchableOpacity>
          </View>
        </View>
        
      </ScrollView>
    </SafeAreaView>
  )
}

export default Analysis
