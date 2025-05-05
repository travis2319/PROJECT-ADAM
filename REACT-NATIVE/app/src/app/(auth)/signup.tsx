import { SafeAreaView } from 'react-native-safe-area-context'
import Signup from '@/screens/auth/SignUp'

const signup = () => {
  return (
    <SafeAreaView className='flex-1'>
        <Signup/>
    </SafeAreaView>
  )
}

export default signup