import React from 'react';
import { Image, Text, View, StatusBar, ScrollView, TouchableOpacity } from 'react-native';
import { Ionicons,MaterialCommunityIcons,FontAwesome, Feather } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useAuth } from '@/providers/AuthProvider';
import { Link, router, useRouter } from 'expo-router';

export default function Home() {
  const {user} = useAuth();
  let currentDate = new Date();
  return (
    <>
      <StatusBar
        backgroundColor="#f4f1de"
        barStyle="dark-content"  // This makes status bar elements black
      />
      <SafeAreaView className="flex-1">
        <ScrollView className="bg-[#f4f1de] px-5 flex-1">
          {/* Header Section */}
          <View className="flex flex-row items-center mt-5 mb-5">
            <Image
              source={require('../../assets/images/profile.jpeg')}
              className="w-10 h-10 rounded-full mr-2"
            />
            <View>
              <Text className="text-lg font-bold text-black">Hello, {user?.name}</Text>
                <Text className="text-sm text-gray-600">
                {currentDate.toLocaleDateString('en-GB', {
                  day: '2-digit',
                  month: 'short',
                  year: 'numeric',
                })}
                </Text>
            </View>
            {/* <TouchableOpacity className='ml-auto'>
              <Ionicons name="search" size={24} color="black" />
            </TouchableOpacity> */}
            {/* <Link href="../maps/1">maps</Link> */}
            <TouchableOpacity className='ml-auto' onPress={() => router.push('../maps/1')}>
              <Feather name="map-pin" size={24} color="black" />
            </TouchableOpacity>
          </View>

          {/* Daily Challenge Section */}
          <View className="bg-[#e5d0ff] rounded-xl p-5 mb-5">
            <Text className="text-2xl font-bold text-black">Daily challenge</Text>
            <Text className="text-lg text-gray-600 my-2">Do your plan before 09:00 AM</Text>
            <View className="flex flex-row items-center">
              <Image
                source={require('../../assets/images/engine.jpg')} // Replace with avatar image URL
                className="w-10 h-10 rounded-full mr-1"
              />
              <Image
                source={require('../../assets/images/engine.jpg')} // Replace with avatar image URL
                className="w-10 h-10 rounded-full mr-1"
              />
              <Image
                source={require('../../assets/images/engine.jpg')} // Replace with avatar image URL
                className="w-10 h-10 rounded-full mr-1"
              />
              <Text className="text-lg font-bold text-gray-600">+4</Text>
            </View>
          </View>

          {/* Date Picker Section */}
          <View className="flex flex-row justify-between mb-5">
            {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day, index) => (
              <View
                key={index}
                className={`flex flex-col items-center py-2 ${day === 'Wed' ? 'bg-black rounded-full px-3' : ''}`}
              >
                <Text
                  className={`text-sm ${day === 'Wed' ? 'text-white' : 'text-gray-600'}`}
                >
                  {day[0]}
                </Text>
                <Text
                  className={`text-lg ${day === 'Wed' ? 'text-white' : 'text-gray-600'}`}
                >
                  {23 + index}
                </Text>
              </View>
            ))}
          </View>

            {/* Your Car Status Section */}
            <View className="mb-5">
              <Text className="text-2xl font-bold text-black mb-3">Car status</Text>
              <View className="flex flex-row justify-between">
              {/* RPM Card */}
              <View className="w-[48%] bg-[#ffdeaf] rounded-xl p-6">
              <View className="flex flex-row items-center mb-2">
              <MaterialCommunityIcons name="speedometer" size={24} color="black" />
              <Text className="text-lg font-bold ml-2">RPM</Text>
              </View>
              <Text className="text-xl text-black mb-2">3000</Text>
              <Text className="text-md text-gray-600">Timestamp: 25 Nov. 14:00</Text>
              </View>
              {/* Coolant Temp Card */}
              <View className="w-[48%] bg-[#d0f4ff] rounded-xl p-6">
              <View className="flex flex-row items-center mb-2">
              <FontAwesome name="thermometer-4" size={24} color="black" />
              <Text className="text-lg font-bold ml-2">Coolant Temp</Text>
              </View>
              <Text className="text-xl text-black mb-2">90°C</Text>
              <Text className="text-md text-gray-600">Timestamp: 28 Nov. 18:00</Text>
              </View>
              </View>
            </View>

        </ScrollView>
      </SafeAreaView>
    
    </>
  );
}
