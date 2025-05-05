// useForm.ts
import { useState } from "react";

export interface FormData {
    name?: string
    email: string;
    username?: string;
    password: string;
    confirmPassword?: string;
  }
  
  const useForm = (initialState: FormData) => {
    const [formData, setFormData] = useState<FormData>(initialState);
  
    const handleChange = (name: keyof FormData, value: string) => {
      setFormData((prevState) => ({
        ...prevState,
        [name]: value,
      }));
    };
  
    return [formData, handleChange] as const; // Use 'as const' for tuple return type
  };
  
  export default useForm;
  