import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import Markdown from 'react-native-markdown-display'; // Import react-native-markdown-display

const ChatScreen: React.FC = () => {
  const [query, setQuery] = useState<string>('');
  const [response, setResponse] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const userId: string = 'VOID-001'; // Ideally, get this from your auth context
  const currentTime: string = new Date().toISOString();

  const baseUrl: string = 'http://192.168.242.63:8000';

  const handleSendQuery = async () => {
    if (!query) return;

    setLoading(true);
    try {
      const encodedQuery: string = encodeURIComponent(query);
      const url: string = `${baseUrl}/chatbot/ask?query=${encodedQuery}&user_id=${userId}&current_time=${currentTime}`;

      // Replace 'user' and 'password' with your actual credentials
      const username = 'user';
      const password = 'password';
      const encodedCredentials = btoa(`${username}:${password}`); // Base64 encode credentials

      const apiResponse = await fetch(url, {
        method: 'GET',
        headers: {
          'accept': 'application/json',
          'Authorization': `Basic ${encodedCredentials}`, // Add the Authorization header
        },
      });

      if (!apiResponse.ok) {
        throw new Error(`HTTP error! Status: ${apiResponse.status}`);
      }

      const data = await apiResponse.json();
      console.log('Chatbot Response:', data);
      setResponse(data.response || 'No response received.'); // Handle cases where response might be null
    } catch (error: any) {
      console.error('Error fetching chatbot response:', error);
      Alert.alert(
        'Error',
        'Failed to get response from the server. Please check your connection and try again.',
      ); // User-friendly error message
      setResponse('Error fetching response. Please try again.');
    } finally {
      setLoading(false);
      setQuery(''); // Clear the input after sending, regardless of success/failure
    }
  };


  const handleButtonClick = (buttonText: string) => {
    setQuery(buttonText);
  };

  return (
    <SafeAreaView className="flex-1 bg-[#f4f1de] px-4">
      <View className="flex-1">
        <View className="items-center mt-8">
          <Text className="text-2xl font-bold text-black">How can we Help You?</Text>
          <Text className="text-sm text-gray-700 mt-1">Predictions</Text>
        </View>

        {/* Centered Buttons */}
        <View className="mt-6 flex-1 justify-center gap-4">
          <View className="flex-row justify-center gap-4">
            <TouchableOpacity
              onPress={() => handleButtonClick('Spark Plug Replacement')}
              className="bg-[#eee5db] px-4 py-3 rounded-lg shadow-md"
            >
              <Text className="text-black">Spark Plug Replacement</Text>
            </TouchableOpacity>
            <TouchableOpacity
              onPress={() => handleButtonClick('Air Filter Replacement')}
              className="bg-[#eee5db] px-4 py-3 rounded-lg shadow-md"
            >
              <Text className="text-black">Air Filter Replacement</Text>
            </TouchableOpacity>
          </View>

          <View className="flex-row justify-center gap-4">
            <TouchableOpacity
              onPress={() => handleButtonClick('Battery Health')}
              className="bg-[#faf4ce] px-4 py-3 rounded-lg shadow-md"
            >
              <Text className="text-black">Battery Health</Text>
            </TouchableOpacity>
            <TouchableOpacity
              onPress={() => handleButtonClick('Coolant Change')}
              className="bg-[#faf4ce] px-4 py-3 rounded-lg shadow-md"
            >
              <Text className="text-black">Coolant Change</Text>
            </TouchableOpacity>
          </View>

          <View className="flex-row justify-center gap-4">
            <TouchableOpacity
              onPress={() => handleButtonClick('Estimate Oil Change')}
              className="bg-[#f4d7c3] px-4 py-3 rounded-lg shadow-md"
            >
              <Text className="text-black">Estimate Oil Change</Text>
            </TouchableOpacity>
            <TouchableOpacity
              onPress={() => handleButtonClick('Estimate Brake Pad Wear')}
              className="bg-[#f4d7c3] px-4 py-3 rounded-lg shadow-md"
            >
              <Text className="text-black">Estimate Brake Pad Wear</Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* Display Response as Markdown */}
        <ScrollView className="mt-4">
          <Markdown>{response}</Markdown>
        </ScrollView>

        {/* Input Field at Bottom */}
        <KeyboardAvoidingView
          behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
          style={{ marginBottom: 90 }} // Adjust margin to position above tab bar
        >
          <View className="bg-[#e6dfd3] flex-row items-center px-4 py-3 rounded-lg shadow-md">
            <TextInput
              placeholder="Ask Query"
              placeholderTextColor="#000"
              className="flex-1 text-black"
              style={{ height: 40 }} // Set a fixed height for the input
              value={query}
              onChangeText={(text) => setQuery(text)}
            />
            <TouchableOpacity onPress={handleSendQuery} disabled={loading}>
              {loading ? (
                <ActivityIndicator size="small" color="#5a503d" />
              ) : (
                <Ionicons name="search" size={30} color="#5a503d" />
              )}
            </TouchableOpacity>
          </View>
        </KeyboardAvoidingView>
      </View>
    </SafeAreaView>
  );
};

export default ChatScreen;


// import React, { useState } from 'react';
// import {
//   View,
//   Text,
//   TextInput,
//   TouchableOpacity,
//   KeyboardAvoidingView,
//   Platform,
//   ScrollView,
//   ActivityIndicator,
//   Alert,
// } from 'react-native';
// import { SafeAreaView } from 'react-native-safe-area-context';
// import { Ionicons } from '@expo/vector-icons';

// const ChatScreen = () => {
//   const [query, setQuery] = useState('');
//   const [response, setResponse] = useState('');
//   const [loading, setLoading] = useState(false);
//   const userId = 'VOID-001'; // Ideally, get this from your auth context
//   const currentTime = new Date().toISOString();

//   const baseUrl = 'http://192.168.251.63:8000';

//   // const handleSendQuery = async () => {
//   //   if (!query) return;

//   //   setLoading(true);
//   //   try {
//   //     const encodedQuery = encodeURIComponent(query);
//   //     const url = `${baseUrl}/chatbot/ask?query=${encodedQuery}&user_id=${userId}&current_time=${currentTime}`;

//   //     const apiResponse = await fetch(url, {
//   //       method: 'GET',
//   //       headers: {
//   //         'accept': 'application/json',
//   //       },
//   //     });

//   //     if (!apiResponse.ok) {
//   //       throw new Error(`HTTP error! Status: ${apiResponse.status}`);
//   //     }

//   //     const data = await apiResponse.json();
//   //     console.log('Chatbot Response:', data);
//   //     setResponse(data.response || 'No response received.'); // Handle cases where response might be null
//   //   } catch (error) {
//   //     console.error('Error fetching chatbot response:', error);
//   //     Alert.alert(
//   //       'Error',
//   //       'Failed to get response from the server. Please check your connection and try again.',
//   //     ); // User-friendly error message
//   //     setResponse('Error fetching response. Please try again.');
//   //   } finally {
//   //     setLoading(false);
//   //     setQuery(''); // Clear the input after sending, regardless of success/failure
//   //   }
//   // };

//   const handleSendQuery = async () => {
//     if (!query) return;

//     setLoading(true);
//     try {
//       const encodedQuery = encodeURIComponent(query);
//       const url = `${baseUrl}/chatbot/ask?query=${encodedQuery}&user_id=${userId}&current_time=${currentTime}`;

//       // Replace 'user' and 'password' with your actual credentials
//       const username = 'user';
//       const password = 'password';
//       const encodedCredentials = btoa(`${username}:${password}`); // Base64 encode credentials

//       const apiResponse = await fetch(url, {
//         method: 'GET',
//         headers: {
//           'accept': 'application/json',
//           'Authorization': `Basic ${encodedCredentials}`, // Add the Authorization header
//         },
//       });

//       if (!apiResponse.ok) {
//         throw new Error(`HTTP error! Status: ${apiResponse.status}`);
//       }

//       const data = await apiResponse.json();
//       console.log('Chatbot Response:', data);
//       setResponse(data.response || 'No response received.'); // Handle cases where response might be null
//     } catch (error) {
//       console.error('Error fetching chatbot response:', error);
//       Alert.alert(
//         'Error',
//         'Failed to get response from the server. Please check your connection and try again.',
//       ); // User-friendly error message
//       setResponse('Error fetching response. Please try again.');
//     } finally {
//       setLoading(false);
//       setQuery(''); // Clear the input after sending, regardless of success/failure
//     }
//   };


//   const handleButtonClick = (buttonText: React.SetStateAction<string>) => {
//     setQuery(buttonText);
//   };

//   return (
//     <SafeAreaView className="flex-1 bg-[#f4f1de] px-4">
//       <View className="flex-1">
//         <View className="items-center mt-8">
//           <Text className="text-2xl font-bold text-black">How can we Help You?</Text>
//           <Text className="text-sm text-gray-700 mt-1">Predictions</Text>
//         </View>

//         {/* Centered Buttons */}
//         <View className="mt-6 flex-1 justify-center gap-4">
//           <View className="flex-row justify-center gap-4">
//             <TouchableOpacity
//               onPress={() => handleButtonClick('Spark Plug Replacement')}
//               className="bg-[#eee5db] px-4 py-3 rounded-lg shadow-md"
//             >
//               <Text className="text-black">Spark Plug Replacement</Text>
//             </TouchableOpacity>
//             <TouchableOpacity
//               onPress={() => handleButtonClick('Air Filter Replacement')}
//               className="bg-[#eee5db] px-4 py-3 rounded-lg shadow-md"
//             >
//               <Text className="text-black">Air Filter Replacement</Text>
//             </TouchableOpacity>
//           </View>

//           <View className="flex-row justify-center gap-4">
//             <TouchableOpacity
//               onPress={() => handleButtonClick('Battery Health')}
//               className="bg-[#faf4ce] px-4 py-3 rounded-lg shadow-md"
//             >
//               <Text className="text-black">Battery Health</Text>
//             </TouchableOpacity>
//             <TouchableOpacity
//               onPress={() => handleButtonClick('Coolant Change')}
//               className="bg-[#faf4ce] px-4 py-3 rounded-lg shadow-md"
//             >
//               <Text className="text-black">Coolant Change</Text>
//             </TouchableOpacity>
//           </View>

//           <View className="flex-row justify-center gap-4">
//             <TouchableOpacity
//               onPress={() => handleButtonClick('Estimate Oil Change')}
//               className="bg-[#f4d7c3] px-4 py-3 rounded-lg shadow-md"
//             >
//               <Text className="text-black">Estimate Oil Change</Text>
//             </TouchableOpacity>
//             <TouchableOpacity
//               onPress={() => handleButtonClick('Estimate Brake Pad Wear')}
//               className="bg-[#f4d7c3] px-4 py-3 rounded-lg shadow-md"
//             >
//               <Text className="text-black">Estimate Brake Pad Wear</Text>
//             </TouchableOpacity>
//           </View>
//         </View>

//         {/* Display Response */}
//         <ScrollView className="mt-4">
//           <Text className="text-black">{response}</Text>
//         </ScrollView>

//         {/* Input Field at Bottom */}
//         <KeyboardAvoidingView
//           behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
//           style={{ marginBottom: 90 }} // Adjust margin to position above tab bar
//         >
//           <View className="bg-[#e6dfd3] flex-row items-center px-4 py-3 rounded-lg shadow-md">
//             <TextInput
//               placeholder="Ask Query"
//               placeholderTextColor="#000"
//               className="flex-1 text-black"
//               style={{ height: 40 }} // Set a fixed height for the input
//               value={query}
//               onChangeText={(text) => setQuery(text)}
//             />
//             <TouchableOpacity onPress={handleSendQuery} disabled={loading}>
//               {loading ? (
//                 <ActivityIndicator size="small" color="#5a503d" />
//               ) : (
//                 <Ionicons name="search" size={30} color="#5a503d" />
//               )}
//             </TouchableOpacity>
//           </View>
//         </KeyboardAvoidingView>
//       </View>
//     </SafeAreaView>
//   );
// };

// export default ChatScreen;
