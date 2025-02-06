import { View, Text } from 'react-native'
import React from 'react'
import Home from '@/screens/tabs/Home'
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context'

const index = () => {
  return (
    <SafeAreaView className='flex-1'>
      <Home/>
    </SafeAreaView>
  )
}

export default index