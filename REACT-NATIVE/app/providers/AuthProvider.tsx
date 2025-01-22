// import React, {
//     createContext,
//     ReactNode,
//     useContext,
//     useState,
//     useEffect,
//   } from "react";
//   import { supabase } from "@/utils/supabase";
//   import { useRouter } from "expo-router";
//   import { User } from "@supabase/supabase-js";
  
//   interface AuthContextType {
//     user: User | null;
//     signIn: (email: string, password: string) => Promise<void>;
//     signUp: (username: string, email: string, password: string) => Promise<void>;
//     completeOnboarding: ()=> Promise<void>;
//     signOut: () => Promise<void>;
//   }
  
//   const AuthContext = createContext<AuthContextType>({
//     user: null,
//     signIn: async () => {},
//     signUp: async () => {},
//     signOut: async () => {},
//   });
  
//   export const useAuth = () => useContext(AuthContext);
  
//   export const AuthProvider: React.FC<{ children: ReactNode }> = ({
//     children,
//   }) => {
//     const [user, setUser] = useState<User | null>(null);
//     const router = useRouter();
  
//     useEffect(() => {
//       const { data: authData } = supabase.auth.onAuthStateChange(
//         (event, session) => {
//           if (!session) return router.push("/(auth)");
//           getUser(session?.user?.id);
//         }
//       );
//       return () => {
//         authData.subscription.unsubscribe();
//       };
//     }, []);
  
//     const getUser = async (id: string) => {
//       const { data, error } = await supabase
//         .from("User")
//         .select("*")
//         .eq("id", id)
//         .single();
  
//       if (error) {
//         console.error("Error fetching user:", error);
//         return;
//       }
//       setUser(data);
//       console.log(data);
      
//       // router.push("/(tabs)");
//       if (data.hasCompletedOnboarding) {
//         router.push("/(tabs)"); // Home
//       } else {
//         router.push("/(onboarding)"); // Onboarding
//       }
//     };
  
//     const signIn = async (email: string, password: string) => {
//       const { data, error } = await supabase.auth.signInWithPassword({
//         email,
//         password,
//       });
  
//       if (error) {
//         console.error("Sign in error:", error);
//         throw error; // Propagate error to caller
//       }
  
//       console.log("Login successful");
//       if (data.user) {
//         getUser(data.user.id);
//       }
//     };
  
//     const signUp = async (username: string, email: string, password: string) => {
//       const { data, error } = await supabase.auth.signUp({ email, password });
//       console.log(username,email,password);
      
//       if (error) {
//         console.log(error);
        
//         console.error("Sign up error:", error);
//         throw error; // Propagate error to caller
//       }
  
//       if (!data.user) {
//         throw new Error("User data is missing after sign up");
//       }
  
//       const { error: userError } = await supabase.from("User").insert({
//         id: data.user.id,
//         username,
//         email,
//         // role: 'ENTHUSIAST',
//       });
  
//       if (userError) {
//         console.error("Error creating user profile:", userError);
//         throw userError; // Propagate error to caller
//       }
  
//       if (data.user) {
//         getUser(data.user.id);
//       }
//       console.log("Sign up successful");
//       router.push("/(onboarding)");
//     };
  
//     const completeOnboarding = async () => {
//       if (!user) return;
    
//       const { error } = await supabase
//         .from("User")
//         .update({ hasCompletedOnboarding: true })
//         .eq("id", user.id);
    
//       if (error) {
//         console.error("Error updating onboarding status:", error);
//         throw error; // Propagate error to caller
//       }
    
//       console.log("Onboarding completed");
//       router.push("/(tabs)"); // Navigate to home after completing onboarding
//     };
  
//     const signOut = async () => {
//       const { error } = await supabase.auth.signOut();
  
//       if (error) {
//         console.error("Sign out error:", error);
//         throw error; // Propagate error to caller
//       }
  
//       setUser(null);
//       router.push("/(auth)");
//     };
  
//     return (
//       <AuthContext.Provider value={{ user, signIn, signOut, signUp }}>
//         {children}
//       </AuthContext.Provider>
//     );
//   };
  