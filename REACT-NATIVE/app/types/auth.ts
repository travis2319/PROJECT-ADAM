// types/auth.ts
export type UserType = {
    id: string;
    name: string;
    email: string;
    profileImage?: string;
    phoneNumber?: string;
    role?: 'user' | 'admin';
    createdAt?: Date;
    updatedAt?: Date;
    preferences?: UserPreferences;
    // Add other user properties as needed
  };
  
  export type UserPreferences = {
    notifications: boolean;
    darkMode: boolean;
    language: string;
  };
  
  export type AuthState = {
    user: UserType | null;
    token: string | null;
    isLoading: boolean;
    isAuthenticated: boolean;
    error: string | null;
  };
  
  export type AuthAction = 
    | { type: 'LOGIN_START' }
    | { type: 'LOGIN_SUCCESS'; payload: { user: UserType; token: string } }
    | { type: 'LOGIN_FAILURE'; payload: string }
    | { type: 'LOGOUT' }
    | { type: 'SIGNUP_START' }
    | { type: 'SIGNUP_SUCCESS'; payload: { user: UserType; token: string } }
    | { type: 'SIGNUP_FAILURE'; payload: string }
    | { type: 'UPDATE_USER'; payload: UserType }
    | { type: 'CLEAR_ERROR' };
  
  export type AuthContextType = {
    user: UserType | null;
    isLoading: boolean;
    isAuthenticated: boolean;
    error: string | null;
    login: (email: string, password: string) => Promise<void>;
    signup: (userData: Partial<UserType> & { password: string }) => Promise<void>;
    logout: () => void;
    updateUser: (userData: Partial<UserType>) => Promise<void>;
    clearError: () => void;
  };