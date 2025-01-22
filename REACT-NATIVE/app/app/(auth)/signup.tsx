import { View, Text, TouchableOpacity, Image, StatusBar, TextInput, Alert } from 'react-native';
import React, { useState } from 'react';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useAuth } from '@/providers/AuthProvider';
import { supabase } from '@/utils/supabase';

const useForm = (initialState) => {
  const [formData, setFormData] = useState(initialState);

  const handleChange = (name, value) => {
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  return [formData, handleChange];
};

const Signup = () => {
  const router = useRouter();
  const [formData, handleChange] = useForm({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const { signUp } = useAuth();

  const handleSignUp = async () => {
    if (formData.password !== formData.confirmPassword) {
      Alert.alert('Error', 'Passwords do not match. Please try again.');
      return;
    }
    console.log(formData);
    
    signUp(formData.name, formData.email, formData.password);
  };

  return (
    <SafeAreaView className="flex-1 bg-white">
      <View className="flex justify-center items-center h-full px-6">
        <Text className="text-3xl font-bold text-black mb-4">SIGN UP</Text>
        <Text className="text-md text-center text-gray-600 mb-6">
          Create your account
        </Text>

        {[
          { name: 'name', placeholder: 'Full Name', secureTextEntry: false },
          { name: 'email', placeholder: 'Email', secureTextEntry: false },
          { name: 'password', placeholder: 'Password', secureTextEntry: true },
          { name: 'confirmPassword', placeholder: 'Confirm Password', secureTextEntry: true }
        ].map((field) => (
          <TextInput
            key={field.name}
            value={formData[field.name]}
            placeholder={field.placeholder}
            secureTextEntry={field.secureTextEntry}
            onChangeText={(value) => handleChange(field.name, value)}
            className="bg-gray-100 p-4 mb-4 rounded-lg border border-gray-300 w-full"
          />
        ))}

        <TouchableOpacity 
          className="bg-blue-500 p-4 rounded-lg w-full mb-4"
          onPress={handleSignUp}
        >
          <Text className="text-white text-center font-medium">Sign Up</Text>
        </TouchableOpacity>

        <View className="mt-4">
          <Text className="text-center text-gray-600">
            Already have an account?{' '}
            <Text
              onPress={() => router.push('/(auth)')}
              className="text-blue-500 underline font-bold"
            >
              Login
            </Text>
          </Text>
        </View>
      </View>
      <StatusBar />
    </SafeAreaView>
  );
};

export default Signup;
