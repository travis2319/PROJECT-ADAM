import { SafeAreaView } from 'react-native-safe-area-context'
import SignUp from '@/screens/auth/SignUp'

const signup = () => {
  return (
    <SafeAreaView className='flex-1'>
        <SignUp/>
    </SafeAreaView>
  )
}

export default signup