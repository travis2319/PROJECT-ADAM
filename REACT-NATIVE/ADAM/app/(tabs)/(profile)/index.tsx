import { View, Text } from 'react-native'
import React from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'
import Profile from '@/screens/tabs/Profile'

const index = () => {
  return (
    <SafeAreaView>
        <Profile />
    </SafeAreaView>
  )
}

export default index