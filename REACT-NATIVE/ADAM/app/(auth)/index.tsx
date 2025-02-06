import { SafeAreaView } from 'react-native-safe-area-context'
import Login from '@/screens/auth/Login'
import { View,Text } from 'react-native'

const index = () => {
  return (
    <SafeAreaView className='flex-1 justify-center items-center '>
      <Login />
        {/* <View>
          <Text className='text-white'>Hello</Text>
        </View> */}
    </SafeAreaView>
  )
}

export default index