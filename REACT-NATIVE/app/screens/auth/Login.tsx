import { View, Text, TextInput, TouchableOpacity, Image } from 'react-native';
import React, { useState } from 'react';
import { useRouter } from 'expo-router';
import { useColorScheme } from 'react-native';
import { useAuth } from '@/providers/AuthProvider';
import useForm from '@/hooks/useForm';

const Login = () => {
  const router = useRouter();
  const colorScheme = useColorScheme();
  const isDarkMode = colorScheme === 'dark';

  const { signIn } = useAuth(); // Get signIn function from AuthProvider

  const [formData, handleChange] = useForm({ email: "", password: "" });

  const handleSignIn = () => {
    signIn(formData.email, formData.password);
  };


  return (
    <View className={`flex-1 justify-center items-center ${isDarkMode ? 'bg-gray-900' : 'bg-yellow-50'} px-6`}>
      <View className={`w-full max-w-sm p-6 rounded-lg shadow-lg ${isDarkMode ? 'bg-gray-800' : 'bg-white'}`}>
        <Text className={`text-2xl font-bold text-center ${isDarkMode ? 'text-white' : 'text-black'}`}>
          Sports Buddy
        </Text>
        <Text className={`text-center mt-1 ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
          Sign in to your account
        </Text>

        {/* Email Input */}
        <View className="mt-4">
          <Text className={`${isDarkMode ? 'text-gray-300' : 'text-gray-700'} mb-1`}>Email</Text>
          <TextInput
            className={`border p-3 rounded-lg ${isDarkMode ? 'border-gray-600 bg-gray-700 text-white' : 'border-gray-300 bg-white text-black'}`}
            placeholder="Enter your email"
            placeholderTextColor={isDarkMode ? 'gray' : 'black'}
            value={formData.email}
            onChangeText={(value)=>handleChange("email",value)} // Update state on change
          />
        </View>

        {/* Password Input */}
        <View className="mt-3">
          <Text className={`${isDarkMode ? 'text-gray-300' : 'text-gray-700'} mb-1`}>Password</Text>
          <TextInput
            className={`border p-3 rounded-lg ${isDarkMode ? 'border-gray-600 bg-gray-700 text-white' : 'border-gray-300 bg-white text-black'}`}
            placeholder="Enter your password"
            placeholderTextColor={isDarkMode ? 'gray' : 'black'}
            secureTextEntry
            value={formData.password}
            onChangeText={(value)=>handleChange('password',value)} // Update state on change
          />
        </View>

        {/* Sign In Button */}
        <TouchableOpacity className="bg-black py-3 rounded-lg mt-4" onPress={handleSignIn}>
          <Text className="text-white text-center font-semibold">Sign In</Text>
        </TouchableOpacity>

        {/* OR Continue With */}
        <View className="flex flex-row items-center my-4">
          <View className="flex-1 h-[1px] bg-gray-400"></View>
          <Text className={`mx-2 ${isDarkMode ? 'text-gray-300' : 'text-gray-500'}`}>OR CONTINUE WITH</Text>
          <View className="flex-1 h-[1px] bg-gray-400"></View>
        </View>

        {/* Social Buttons */}
        <View className="flex-row space-x-4 gap-4">
          <TouchableOpacity 
            className={`flex-1 border py-3 rounded-lg flex-row items-center justify-center ${isDarkMode ? 'border-gray-500' : 'border-gray-300'}`}
            onPress={()=>{console.log('Google Sign In');}}
          >
            <Image source={require('@/assets/images/google.png')} className="w-6 h-6 mr-2" />
            <Text className={`${isDarkMode ? 'text-white' : 'text-black'} text-center`}>Google</Text>
          </TouchableOpacity>
          <TouchableOpacity 
            className={`flex-1 border py-3 rounded-lg flex-row items-center justify-center ${isDarkMode ? 'border-gray-500' : 'border-gray-300'}`}
            onPress={()=>{console.log('Facebook Sign In');}}
          >
            <Image source={require('@/assets/images/meta.png')} className="w-6 h-6 mr-2" />
            <Text className={`${isDarkMode ? 'text-white' : 'text-black'} text-center`}>Facebook</Text>
          </TouchableOpacity>
        </View>

        {/* Signup Navigation */}
        <TouchableOpacity onPress={() => router.push('/signup')}>
          <Text className={`text-center mt-4 ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
            Don't have an account? <Text className="text-blue-500">Create one</Text>
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

export default Login;