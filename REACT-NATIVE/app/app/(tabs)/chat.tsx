import { View, Text, TextInput, TouchableOpacity, KeyboardAvoidingView, Platform } from 'react-native';
import React from 'react';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';

const ChatScreen = () => {
  return (
    <SafeAreaView className="flex-1 bg-[#f4f1de] px-4">
      <View className="flex-1">
        <View className="items-center mt-8">
          <Text className="text-2xl font-bold text-black">How can we Help You?</Text>
          <Text className="text-sm text-gray-700 mt-1">Predictions</Text>
        </View>

        {/* Centered Buttons */}
        <View className="mt-6 flex-1 justify-center gap-4">
          <View className="flex-row justify-center gap-4">
            <TouchableOpacity className="bg-[#eee5db] px-4 py-3 rounded-lg shadow-md">
              <Text className="text-black">Spark Plug Replacement</Text>
            </TouchableOpacity>
            <TouchableOpacity className="bg-[#eee5db] px-4 py-3 rounded-lg shadow-md">
              <Text className="text-black">Air Filter Replacement</Text>
            </TouchableOpacity>
          </View>

          <View className="flex-row justify-center gap-4">
            <TouchableOpacity className="bg-[#faf4ce] px-4 py-3 rounded-lg shadow-md">
              <Text className="text-black">Battery Health</Text>
            </TouchableOpacity>
            <TouchableOpacity className="bg-[#faf4ce] px-4 py-3 rounded-lg shadow-md">
              <Text className="text-black">Coolant Change</Text>
            </TouchableOpacity>
          </View>

          <View className="flex-row justify-center gap-4">
            <TouchableOpacity className="bg-[#f4d7c3] px-4 py-3 rounded-lg shadow-md">
              <Text className="text-black">Estimate Oil Change</Text>
            </TouchableOpacity>
            <TouchableOpacity className="bg-[#f4d7c3] px-4 py-3 rounded-lg shadow-md">
              <Text className="text-black">Estimate Brake Pad Wear</Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* Input Field at Bottom */}
        <KeyboardAvoidingView 
          behavior={Platform.OS === "ios" ? "padding" : "height"}
          style={{ marginBottom: 90 }} // Adjust margin to position above tab bar
        >
          <View className="bg-[#e6dfd3] flex-row items-center px-4 py-3 rounded-lg shadow-md">
            <TextInput
              placeholder="Ask Query"
              placeholderTextColor="#000"
              className="flex-1 text-black"
              style={{ height: 40 }} // Set a fixed height for the input
            />
            <TouchableOpacity>
              <Ionicons name='search' size={30} color="#5a503d" />
            </TouchableOpacity>
          </View>
        </KeyboardAvoidingView>
      </View>
    </SafeAreaView>
  );
};

export default ChatScreen;
