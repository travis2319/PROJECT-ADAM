import { View, Text, TouchableOpacity, Image } from 'react-native'
import React, { useState } from 'react'
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';

const useForm = (initialState: { email: string; password: string }) => {
    const [formData, setFormData] = useState(initialState);
  
    const handleChange = (name: any, value: any) => {
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
        email: "",
        password: "",
    });

    return (
        <SafeAreaView>
            {/* Main Container */}
            <View className="flex justify-center items-center h-screen">
                {/* Title */}
                <Text className="text-3xl font-bold text-white">LOGIN</Text>

                {/* Social Login Buttons */}
                <View className="flex-row justify-between p-3">
                    <TouchableOpacity 
                        className="flex-1 bg-gray-100 p-3 rounded-lg mr-2 flex-row items-center justify-center"
                        onPress={() => router.push("/(tabs)")}
                    >
                        <Image 
                            source={require('../../assets/images/google_logo.png')} 
                            style={{ width: 20, height: 20, marginRight: 8 }} 
                        />
                        <Text className="text-black font-medium">Google</Text>
                    </TouchableOpacity>
                    <TouchableOpacity 
                        className="flex-1 bg-gray-100 p-3 rounded-lg ml-2 flex-row items-center justify-center"
                        onPress={() => router.push("/(tabs)")}
                    >
                        <Image 
                            source={require('../../assets/images/meta_logo.png')} 
                            style={{ width: 20, height: 20, marginRight: 8 }} 
                        />
                        <Text className="text-black font-medium">Facebook</Text>
                    </TouchableOpacity>
                </View>

                {/* Signup Link */}
                <View className="mt-4">
                    <Text className="text-center text-gray-600">
                        Don’t have an account?{" "}
                        <Text
                            onPress={() => router.push("/(auth)/signup")}
                            className="text-blue-500 underline font-bold"
                        >Create one
                        </Text>
                    </Text>
                </View>
            </View>
        </SafeAreaView>
    );
};

export default Index