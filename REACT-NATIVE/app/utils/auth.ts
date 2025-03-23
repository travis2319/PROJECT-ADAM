// utils/auth.ts
import * as SecureStore from 'expo-secure-store';

export const getAuthCredentials = async () => {
  try {
    const username = await SecureStore.getItemAsync('auth_username') || 'user';
    const password = await SecureStore.getItemAsync('auth_password') || 'password';
    return btoa(`${username}:${password}`); // Base64 encode credentials
  } catch (error) {
    console.error('Error retrieving auth credentials', error);
    return btoa('user:password'); // Fallback to default, though this is not ideal
  }
};