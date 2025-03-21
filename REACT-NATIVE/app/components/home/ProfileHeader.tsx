// components/home/ProfileHeader.tsx
import React from 'react';
import { View, Text, Image, TouchableOpacity } from 'react-native';
import { UserType } from '@/types/auth';

type ProfileHeaderProps = {
  user?: UserType;
};

export const ProfileHeader: React.FC<ProfileHeaderProps> = ({ user }) => {
  const currentDate = new Date();
  
  return (
    <View className="flex-row p-4 items-center justify-between">
      <View className="flex-row items-center">
        <Image
          source={require('@/assets/images/profile.jpeg')}
          className="w-14 h-14 rounded-full mr-4 border-2 border-[#105e62]"
        />
        <View>
          <Text className="text-[#105e62] text-xl font-bold">Hello, {user?.name || 'User'}</Text>
          <Text className="text-sm text-gray-600">
            {currentDate.toLocaleDateString('en-GB', {
              day: '2-digit',
              month: 'short',
              year: 'numeric',
            })}
          </Text>
        </View>
      </View>
      <TouchableOpacity className="p-2 bg-gray-100 rounded-full">
        <Image
          source={{ uri: 'https://cdn-icons-png.flaticon.com/512/545/545705.png' }}
          className="w-6 h-6 text-gray-500"
        />
      </TouchableOpacity>
    </View>
  );
};