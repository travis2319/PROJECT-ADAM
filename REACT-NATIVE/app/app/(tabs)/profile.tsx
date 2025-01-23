import { View, Text, Image, TouchableOpacity, ScrollView } from 'react-native';
import React from 'react';
import { SafeAreaView } from 'react-native-safe-area-context';

const Profile = () => {
  return (
    <SafeAreaView className="flex-1 bg-[#f1f4de] p-4">
      <ScrollView>
      {/* Header */}
      <View className="flex-row items-center mb-4">
        {/* <TouchableOpacity className="p-2">
        <Text className="text-2xl">←</Text>
        </TouchableOpacity> */}
        {/* <Image
        source={{ uri: 'https://via.placeholder.com/50' }} 
        className="w-12 h-12 rounded-full ml-2"
        /> */}
        <View className="ml-4">
        <Text className="text-xl font-bold">Travis Fernandes</Text>
        <Text className="text-gray-500">GA-09-A-4683  Zen Estilo LXI</Text>
        </View>
        <TouchableOpacity className="ml-auto">
        <Text className="text-xl">✎</Text>
        </TouchableOpacity>
      </View>

      {/* Vehicle Age Card */}
      <View className="bg-yellow-100 p-4 rounded-lg mb-4">
        <Text className="text-gray-600 font-bold">Vehicle Age</Text>
        <Text className="text-lg font-bold">14 years 2 months 12 days</Text>
        <View className="border-b border-black my-2" />
        <Text className="text-gray-600 font-bold">Last Servicing Date</Text>
        <Text className="text-lg font-bold">31st October 2024</Text>
      </View>

      {/* Vehicle Details */}
      <Text className="font-bold text-lg mb-2">Vehicle details</Text>
      <View className="bg-yellow-100 p-4 rounded-lg mb-4">
        <Text className="text-gray-600">Maker Model</Text>
        <Text className="font-bold">
        MARUTI SUZUKI INDIA LTD, ZEN ESTILO LXI MINOR
        </Text>
        <View className="border-b border-black my-2" />
        <View className="flex-row justify-between">
        <Text className="text-gray-600">Vehicle Class</Text>
        <Text className="text-gray-600">Fuel Type</Text>
        </View>
        <View className="flex-row justify-between font-bold">
        <Text className="font-bold">Motor Car (LMV)</Text>
        <Text className="font-bold">PETROL</Text>
        </View>
        <View className="border-b border-black my-2" />
        <Text className="text-gray-600">Registered RTO</Text>
        <Text className="font-bold">DHARBANDORA RTO, Goa</Text>
      </View>

      {/* Insurance Details */}
      <Text className="font-bold text-lg mb-2">Insurance details</Text>
      <View className="bg-yellow-100 p-4 rounded-lg">
        <Text className="text-gray-600">Insurance Company Name</Text>
        <Text className="font-bold">
        The New India Assurance Company Limited
        </Text>
        <View className="border-b border-black my-2" />
        <View className="flex-row justify-between">
        <Text className="text-gray-600">Insurance effective</Text>
        <Text className="text-gray-600">Insurance expiry</Text>
        </View>
        <View className="flex-row justify-between">
        <Text className="font-bold">04-Nov-2024</Text>
        <Text className="font-bold">04-Jan-2026</Text>
        </View>
        <View className="border-b border-black my-2" />
        <Text className="text-gray-600">Insurance policy No.</Text>
        <Text className="font-bold">123x 456x 789xx</Text>
      </View>
      </ScrollView>
    </SafeAreaView>
  );
};

export default Profile;
