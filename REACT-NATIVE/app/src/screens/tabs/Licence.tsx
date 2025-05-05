import { View, Text } from 'react-native'
import React from 'react'
import { useColorScheme } from '@/hooks/useColorScheme'

const Licence = () => {
  const isDarkMode = useColorScheme() === 'dark'
  return (
    <View className='flex-1 items-center justify-center'>
      <Text className={`${isDarkMode ? 'dark-mode' : 'light-mode'} font-bold text-2xl`}>Licence</Text>
    </View>
  )
}

export default Licence