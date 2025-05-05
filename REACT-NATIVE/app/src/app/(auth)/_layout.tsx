import { Stack } from 'expo-router';
import { FadeIn } from 'react-native-reanimated';


export default function () {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ headerShown: false, animation: 'fade' }} />
      <Stack.Screen name="signup" options={{ headerShown: false, animation: 'fade'}} />
    </Stack>
  );
}
