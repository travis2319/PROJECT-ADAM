import { useState } from "react";

// useForm.ts
export interface FormData {
    email: string;
    password: string;
    username?: string;
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
  