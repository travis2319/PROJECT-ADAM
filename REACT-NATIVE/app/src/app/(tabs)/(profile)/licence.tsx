import React from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'
import Licence from '@/screens/tabs/Licence'

const licence = () => {
  return (
    <SafeAreaView className='flex-1 bg-[#f4f1de] p-4'>
      <Licence />
    </SafeAreaView>
  )
}

export default licence