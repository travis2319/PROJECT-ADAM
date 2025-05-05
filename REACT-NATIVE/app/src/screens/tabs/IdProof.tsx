import { View, Text } from 'react-native'
import React from 'react'
import { useColorScheme } from '@/hooks/useColorScheme'

const IdProof = () => {
    const isDarkMode = useColorScheme() === 'dark'
  return (
    <View>
      <Text>IdProof</Text>
    </View>
  )
}

export default IdProof