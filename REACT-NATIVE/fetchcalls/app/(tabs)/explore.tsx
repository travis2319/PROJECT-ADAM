import { View, Text, FlatList, ActivityIndicator, RefreshControl } from 'react-native';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Explore = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchData = async () => {
    try {
      console.log('Fetching data from localhost...');
      const res = await axios.get('http://192.168.0.107:8080/data');
      console.log('Data fetched:', res.data);
      setData(res.data);
    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const onRefresh = React.useCallback(() => {
    setRefreshing(true);
    fetchData();
  }, []);

  const formatValue = (value) => {
    if (value === null) return '-';
    if (typeof value === 'number') {
      return value.toFixed(2);
    }
    return value.toString();
  };

  const renderDataItem = ({ item }) => {
    // Array of sensor data groups
    const sensorGroups = [
      {
        title: "Location & Time",
        data: [
          { label: "Latitude", value: item.latitude },
          { label: "Longitude", value: item.longitude },
          { label: "Timestamp", value: new Date(item.timestamp * 1000).toLocaleTimeString() },
          { label: "GPS Timestamp", value: new Date(item.timestamp_gps * 1000).toLocaleTimeString() }
        ]
      },
      {
        title: "Engine Data",
        data: [
          { label: "RPM", value: item.rpm },
          { label: "Speed", value: item.speed },
          { label: "Engine Load", value: item.engine_load },
          { label: "Throttle Position", value: item.throttle_pos },
          { label: "Coolant Temperature", value: item.coolant_temp }
        ]
      },
      {
        title: "Fuel System",
        data: [
          { label: "Fuel Type", value: item.fuel_type },
          { label: "MAF", value: item.maf },
          { label: "Commanded Equiv Ratio", value: item.commanded_equiv_ratio }
        ]
      }
    ];

    return (
      <View className="mb-4 bg-white rounded-lg shadow-sm border border-gray-200">
        <View className="bg-blue-50 p-3 rounded-t-lg">
          <Text className="text-lg font-bold text-blue-900">
            Reading {new Date(item.timestamp * 1000).toLocaleTimeString()}
          </Text>
        </View>
        
        {sensorGroups.map((group, groupIndex) => (
          <View key={groupIndex} className="p-3">
            <Text className="text-md font-semibold text-gray-700 mb-2">
              {group.title}
            </Text>
            {group.data.map((sensor, sensorIndex) => (
              <View key={sensorIndex} className="flex-row justify-between py-1">
                <Text className="text-gray-600">{sensor.label}:</Text>
                <Text className="text-black font-medium">
                  {formatValue(sensor.value)}
                </Text>
              </View>
            ))}
            {groupIndex < sensorGroups.length - 1 && (
              <View className="border-b border-gray-200 my-2" />
            )}
          </View>
        ))}
      </View>
    );
  };

  if (loading && !refreshing) {
    return (
      <View className="flex-1 justify-center items-center">
        <ActivityIndicator size="large" color="#0000ff" />
      </View>
    );
  }

  return (
    <View className="flex-1 bg-gray-100">
      <Text className="text-xl font-bold text-center py-4">Vehicle Data</Text>
      <FlatList
        data={data}
        keyExtractor={(item, index) => index.toString()}
        renderItem={renderDataItem}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
          />
        }
        contentContainerClassName="px-4"
      />
    </View>
  );
};

export default Explore;