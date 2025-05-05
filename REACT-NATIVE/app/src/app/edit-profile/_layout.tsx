import { View, Text } from 'react-native'
import React from 'react'
import { Stack } from 'expo-router'

const _layout = () => {
  return (
    <Stack>
        <Stack.Screen
            name='edit-profile'
            options={{
                headerTitle: 'Edit Profile',
                headerBackTitle: 'Back',
            }
            }
        />
    </Stack>
  )
}

export default _layout