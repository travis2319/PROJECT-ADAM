import { View, Text } from 'react-native'
import React from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'

const chat = () => {
  return (
    <SafeAreaView>
      <View className='flex justify-center items-center h-screen bg-[#f4f1de] '>
        <Text className='text-4xl font-bold text-black'>Chat</Text>
      </View>
    </SafeAreaView>
  )
}

export default chat