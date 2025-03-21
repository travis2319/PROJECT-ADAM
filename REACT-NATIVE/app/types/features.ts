// types/features.ts
import { ImageSourcePropType } from 'react-native';

export type FeatureType = {
  title: string;
  icon: ImageSourcePropType;
  backgroundColor: string;
  backgroundIcon?: ImageSourcePropType;
  navigateTo?: string;
};

// types/auth.ts
export type UserType = {
  id: string;
  name: string;
  email: string;
  // Add other user properties as needed
};