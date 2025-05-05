import React, {
  createContext,
  ReactNode,
  useContext,
  useState,
  useEffect,
} from "react";
import { supabase } from "@/utils/supabase";
import { useRouter } from "expo-router";
import { User as SupabaseUser } from "@supabase/supabase-js";

interface User {
  id: string;
  email: string;
  name?: string | null;
  createdAt: Date;
  updatedAt: Date;
}

interface AuthContextType {
  user: User | null;
  // session: Session | null;
  // loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (username: string, email: string, password: string) => Promise<void>;
  // completeOnboarding: ()=> Promise<void>;
  signOut: () => Promise<void>;
  updateProfile: (data: { name?: string }) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {

  const [user, setUser] = useState<User | null>(null);
  // const [session, setSession] = useState<Session | null>(null);
  // const [loading, setLoading] = useState(true);
  const router = useRouter();

    const transformUser = async (supabaseUser: SupabaseUser | null) => {
    if (!supabaseUser) return null;

    const { data: profile } = await supabase
      .from('User')
      .select('*')
      .eq('id', supabaseUser.id)
      .single();

    return profile as User;
  };

  useEffect(() => {
    // supabase.auth.getSession().then(async ({ data: { session } }) => {
    //   setSession(session);
    //   const transformedUser = await transformUser(session?.user ?? null);
    //   setUser(transformedUser);
    //   setLoading(false);
    // });

    const { data: authData } = supabase.auth.onAuthStateChange((event, session) => {
        if(!session) return router.push("/(auth)");
        getUser(session.user.id);
      });

    return () => authData.subscription.unsubscribe();
  }, []);

  const getUser = async (id: string) => {
    const { data, error } = await supabase
      .from("User")
      .select("*")
      .eq("id", id)
      .single();

    if (error) return console.error("Error fetching user:", error);

    setUser(data);
    console.log(data);
    
    router.push("/(tabs)");
  };

  
  const signUp = async (username: string, email: string, password: string) => {
    console.log(username,email,password);
    
    const { data, error } = await supabase.auth.signUp({ 
      email, 
      password ,
        options: {
        data: {
          full_name: username,
        },
        },});
    console.log(data);
    
    if (error) return console.error("Sign up error:", error);
  
    const {error: userError} = await supabase.from("User").insert({
      id: data.user?.id,
      name: username,
      email,
    });

    if (userError) return console.error("Error creating user profile:", userError);
    
    
    if (!data.user) {
      throw new Error("User data is missing after sign up");
    }
    
    
    if (data.user) {
      getUser(data.user.id);
    }
    console.log("Sign up successful");
    router.back();
    router.push("/(tabs)")
    // router.push("/(onboarding)");
  };
  
  const signIn = async (email: string, password: string) => {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) {
      console.error("Sign in error:", error);
      throw error; // Propagate error to caller
    }

    console.log("Login successful");
    if (data.user) {
      getUser(data.user.id);
    }
  };

  const signOut = async () => {
    const { error } = await supabase.auth.signOut();

    if (error) return console.error("Sign out error:", error);

    setUser(null);
    router.push("/(auth)");
  };

  const updateProfile = async (data: { name?: string }) => {
    if (!user?.id) throw new Error('No user found');

    const { error } = await supabase
      .from('User')
      .update(data)
      .eq('id', user.id);

    if (error) throw error;
    setUser(user => user ? { ...user, ...data } : null);
  };

   const value = {
    user,
    // session,
    // loading,
    signUp,
    signIn,
    signOut,
    updateProfile,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}