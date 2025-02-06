import { View, Text, TextInput, Button, TouchableOpacity } from 'react-native';
import React, { useState, useEffect } from 'react';
import { useColorScheme } from '@/hooks/useColorScheme';
import { supabase } from '@/utils/supabase';
import { useAuth } from '@/providers/AuthProvider';

const EditProfile = () => {
  const isDarkMode = useColorScheme() === 'dark';
  const {user} = useAuth();
  const [profile, setProfile] = useState({ 
    name: '' 
});

//   useEffect(() => {
//     const fetchProfile = async () => {
//       if (user) {
//         try {
//           const { data, error } = await supabase
//             .from('User')
//             .select('name')
//             .eq('id', user.id);

//           if (error) {
//             throw error;
//           }

//           if (data && data.length > 0) {
//             setProfile(data[0]);
//           }
//         } catch (err) {
//           console.error("Error fetching profile:", err);
//           setError(err.message || "Failed to fetch profile.");
//         }
//       }
//     };

//     fetchProfile();
//   }, []);

  const handleSave = async () => {
    
  };


    function handleInputChange(arg0: string, text: string): void {
        throw new Error('Function not implemented.');
    }

  return (
    <View className={`flex-1 p-5 ${isDarkMode ? 'bg-gray-800' : 'bg-white'}`}>
        <View className="justify-center items-center">
            <Text className={`text-2xl font-bold mb-4 ${isDarkMode ? 'text-white' : 'text-black'}`}>
                Edit Profile
            </Text>
        </View>
      {/* {error && <Text clfassName="text-red-500 mb-2">{error}</Text>} */}

      <TextInput
        className={`border border-gray-300 p-2 mb-4 rounded ${
          isDarkMode ? 'bg-gray-700 text-white border-gray-600' : 'bg-white text-black'
        }`}
        placeholder="Name"
        placeholderTextColor={isDarkMode ? 'gray' : 'black'}
        value={profile.name}
        onChangeText={(text) => handleInputChange('name', text)}
      />

      <TouchableOpacity
        className='bg-blue-500 p-3 rounded items-center justify-center'
      >
        <Text className='font-bold'>Submit</Text>
      </TouchableOpacity>
    </View>
  );
};


export default EditProfile;