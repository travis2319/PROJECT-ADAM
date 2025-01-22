import { View, Text, TouchableOpacity, Image, StatusBar, TextInput } from 'react-native';
import React, { useState } from 'react';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useAuth } from '@/providers/AuthProvider';
// import { supabase } from '@/utils/supabase';

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

const Index = () => {
  const router = useRouter();
  const [formData, handleChange] = useForm({
    email: '',
    password: '',
  });
  const { signIn } = useAuth();

  const handleLogin = async () => {
    console.log('Form Data:', formData);

    if (!formData.email || !formData.password){
      console.log('Error: Email and password are required');
      return;
    }
    signIn(formData.email, formData.password);
  };


  return (
    <>
    <StatusBar
      backgroundColor="#ffffff"
    barStyle="dark-content"  // This makes status bar elements black
    />
    <SafeAreaView className="flex-1 bg-white">
      <View className="flex justify-center items-center h-full px-6">
        <Text className="text-3xl font-bold text-black mb-4">LOGIN</Text>
        <Text className="text-md text-center text-gray-600 mb-6">
          Sign in to your account
        </Text>

        {[{ name: 'email', placeholder: 'Email', secureTextEntry: false },
          { name: 'password', placeholder: 'Password', secureTextEntry: true }]
          .map((field) => (
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
          onPress={() => handleLogin()}
        >
          <Text className="text-white text-center font-medium">Login</Text>
        </TouchableOpacity>

        <View className="flex-row justify-between w-full mb-4">
          <TouchableOpacity 
            className="flex-1 bg-gray-100 p-3 rounded-lg mr-2 flex-row items-center justify-center"
            onPress={() => router.push('/(tabs)')}
          >
            <Image 
              source={require('../../assets/images/google_logo.png')} 
              style={{ width: 20, height: 20, marginRight: 8 }} 
            />
            <Text className="text-black font-medium">Google</Text>
          </TouchableOpacity>
          <TouchableOpacity 
            className="flex-1 bg-gray-100 p-3 rounded-lg ml-2 flex-row items-center justify-center"
            onPress={() => router.push('/(tabs)')}
          >
            <Image 
              source={require('../../assets/images/meta_logo.png')} 
              style={{ width: 20, height: 20, marginRight: 8 }} 
            />
            <Text className="text-black font-medium">Facebook</Text>
          </TouchableOpacity>
        </View>

        <View className="mt-4">
          <Text className="text-center text-gray-600">
            Don’t have an account?{' '}
            <Text
              onPress={() => router.push('/(auth)/signup')}
              className="text-blue-500 underline font-bold"
            >
              Create one
            </Text>
          </Text>
        </View>
      </View>
      <StatusBar />
    </SafeAreaView>
    </>
  );
};

export default Index;