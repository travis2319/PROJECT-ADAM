import { View, Text, TextInput, TouchableOpacity } from 'react-native';
import React from 'react';
import { useRouter } from 'expo-router';
import { useColorScheme } from 'react-native';
import { useAuth } from '@/providers/AuthProvider';
import useForm from '@/hooks/useForm';

const Signup = () => {
  const router = useRouter();
  const { signUp } = useAuth();
  const colorScheme = useColorScheme();
  const isDarkMode = colorScheme === 'dark';

  // Form state using useForm hook
  const [formData, handleChange] = useForm({
    username: "",
    email: "",
    password: "",
  });

  const handleSignup = async () => {
    if (!formData.username || !formData.email || !formData.password) {
      alert("All fields are required.");
      return;
    }
    try {
      await signUp(formData.username, formData.email, formData.password);
      // router.push('/onboarding'); // Navigate only on successful sign-up
    } catch (error) {
      alert("Signup failed. Please try again.");
    }
  };

  return (
    <View className={`flex-1 justify-center items-center ${isDarkMode ? 'bg-gray-900' : 'bg-yellow-50'} px-6`}>
      <View className={`w-full max-w-sm p-6 rounded-lg shadow-lg ${isDarkMode ? 'bg-gray-800' : 'bg-white'}`}>
        <Text className={`text-2xl font-bold text-center ${isDarkMode ? 'text-white' : 'text-black'}`}>
          Create Account
        </Text>
        <Text className={`text-center mt-1 ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
          Sign up to get started
        </Text>

        {/* Username Input */}
        <View className="mt-4">
          <Text className={`${isDarkMode ? 'text-gray-300' : 'text-gray-700'} mb-1`}>Full Name</Text>
          <TextInput
            className={`border p-3 rounded-lg ${isDarkMode ? 'border-gray-600 bg-gray-700 text-white' : 'border-gray-300 bg-white text-black'}`}
            placeholder="John Doe"
            placeholderTextColor={isDarkMode ? 'gray' : 'black'}
            onChangeText={(value) => handleChange('username', value)}
            value={formData.username}
          />
        </View>

        {/* Email Input */}
        <View className="mt-3">
          <Text className={`${isDarkMode ? 'text-gray-300' : 'text-gray-700'} mb-1`}>Email</Text>
          <TextInput
            className={`border p-3 rounded-lg ${isDarkMode ? 'border-gray-600 bg-gray-700 text-white' : 'border-gray-300 bg-white text-black'}`}
            placeholder="m@example.com"
            placeholderTextColor={isDarkMode ? 'gray' : 'black'}
            onChangeText={(value) => handleChange('email', value)}
            value={formData.email}
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
            onChangeText={(value) => handleChange('password', value)}
            value={formData.password}
          />
        </View>

        {/* Signup Button */}
        <TouchableOpacity className="bg-black py-3 rounded-lg mt-4" onPress={handleSignup}>
          <Text className="text-white text-center font-semibold">Sign Up</Text>
        </TouchableOpacity>

        {/* Login Navigation */}
        <TouchableOpacity onPress={() => router.push('/(auth)')}>
          <Text className={`text-center mt-4 ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
            Already have an account? <Text className="text-blue-500">Sign in</Text>
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

export default Signup;
