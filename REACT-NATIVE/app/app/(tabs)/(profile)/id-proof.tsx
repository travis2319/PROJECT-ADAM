import { View, Text } from 'react-native'
import React from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'
import IdProof from '@/screens/tabs/IdProof'

const idproof = () => {
  return (
    <SafeAreaView>
      <IdProof />
    </SafeAreaView>
  )
}

export default idproof