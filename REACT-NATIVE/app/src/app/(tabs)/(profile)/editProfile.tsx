import { View, Text } from 'react-native'
import React from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'
import EditProfile from '@/screens/tabs/EditProfile'

const editProfile = () => {
  return (
    // <SafeAreaView className='flex-1'>
      <EditProfile />
    // </SafeAreaView>
  )
}

export default editProfile