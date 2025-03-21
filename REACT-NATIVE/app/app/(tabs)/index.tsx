// app/(tabs)/index.tsx - Main Home component
import React from 'react';
import { View, SafeAreaView, ScrollView, StatusBar } from 'react-native';
import { ProfileHeader } from '@/components/home/ProfileHeader';
import { CarDisplay } from '@/components/home/CarDisplay';
import { MetricsRow } from '@/components/home/MetricsRow';
import { FeatureGrid } from '@/components/home/FeatureGrid';
import { useAuth } from '@/providers/AuthProvider';
import { useWindowDimensions } from 'react-native';
import { FEATURES_DATA } from '@/constants/homeData';
import { SectionTitle } from '@/components/home/SectionTitle';

export default function Home() {
  const { user } = useAuth();
  const { height } = useWindowDimensions();
  
  return (
    <SafeAreaView className="flex-1 bg-[#f0f4f8] pt-6">
      <ScrollView className="flex-1" showsVerticalScrollIndicator={false}>
        <StatusBar barStyle="dark-content" />
        
        {user && <ProfileHeader user={{ ...user, name: user.name ?? 'Guest' }} />}
        
        <CarDisplay 
          imageUrl="https://th.bing.com/th/id/R.e02339a312d4fa88081615dd587b87ee?rik=Nvb6s7Qnqw99BA&riu=http%3a%2f%2fi.ndtvimg.com%2fauto%2fmakers%2f29%2f198%2fmaruti-estilo.jpg&ehk=idaG%2brreG8tFC9vC6f%2fFB%2bkO7y%2fZwjcLJdW%2bnyFgsI8%3d&risl=&pid=ImgRaw&r=0"
          maxHeight={Math.min(height * 0.25, 200)}
        />
        
        <MetricsRow 
          rpm={{ value: 1173.5, unit: 'rpm' }}
          speed={{ value: 26, unit: 'km/h' }}
        />
        
        <View className="px-6 mt-6">
          <SectionTitle title="Features" />
        </View>
        
        <FeatureGrid 
          features={FEATURES_DATA}
          cardHeight={Math.min(height * 0.18, 200)}
        />
        
        {/* Added bottom padding for scrolling comfort */}
        <View className="h-8" />
      </ScrollView>
    </SafeAreaView>
  );
}

// import React from 'react';
// import { View, Text, Image, SafeAreaView, TouchableOpacity, ScrollView, StatusBar, useWindowDimensions } from 'react-native';
// import icon from "@/assets/images/prof.png";
// import temp from "@/assets/images/temp.png";
// import temp1 from "@/assets/images/temp1.png";
// import car from "@/assets/images/carlog.png";
// import location from "@/assets/images/loc.png";
// import speed from "@/assets/images/speed.png";
// import rpm from "@/assets/images/rpm.png";
// import rpm2 from "@/assets/images/rpm2.png";
// import curv from "@/assets/images/curv.png";
// import speed2 from "@/assets/images/speed2.png";
// import route from "@/assets/images/route.png";
// import carimg from '@/assets/images/estilo.png';
// import { useAuth } from '@/providers/AuthProvider';
// import { Link, router, useRouter } from 'expo-router';

// export default function Home() {
//   const { user } = useAuth();
//   const { height, width } = useWindowDimensions();
//   let currentDate = new Date();
  
//   // Calculate responsive heights based on device screen
//   const carImageHeight = Math.min(height * 0.25, 200); // 25% of screen height, max 200
//   const featureCardHeight = Math.min(height * 0.18, 140); // 18% of screen height, max 140
  
//   return (
//     <SafeAreaView className="flex-1 bg-[#f0f4f8] pt-6">
//       <ScrollView className="flex-1" showsVerticalScrollIndicator={false}>
//         <StatusBar barStyle="dark-content" />
        
//         {/* Profile Header - Enhanced */}
//         <View className="flex-row p-4 items-center justify-between">
//           <View className="flex-row items-center">
//             <Image
//               source={require('../../assets/images/profile.jpeg')}
//               className="w-14 h-14 rounded-full mr-4 border-2 border-[#105e62]"
//             />
//             <View>
//               <Text className="text-[#105e62] text-xl font-bold">Hello, {user?.name}</Text>
//               <Text className="text-sm text-gray-600">
//                 {currentDate.toLocaleDateString('en-GB', {
//                   day: '2-digit',
//                   month: 'short',
//                   year: 'numeric',
//                 })}
//               </Text>
//             </View>
//           </View>
//           <TouchableOpacity className="p-2 bg-gray-100 rounded-full">
//             <Image
//               source={{ uri: 'https://cdn-icons-png.flaticon.com/512/545/545705.png' }}
//               className="w-6 h-6 text-gray-500"
//             />
//           </TouchableOpacity>
//         </View>
        
//         {/* Car Image - Responsive height */}
//         <View className="px-4 -mt-2">
//           <Image 
//             source={{ uri: 'https://th.bing.com/th/id/R.e02339a312d4fa88081615dd587b87ee?rik=Nvb6s7Qnqw99BA&riu=http%3a%2f%2fi.ndtvimg.com%2fauto%2fmakers%2f29%2f198%2fmaruti-estilo.jpg&ehk=idaG%2brreG8tFC9vC6f%2fFB%2bkO7y%2fZwjcLJdW%2bnyFgsI8%3d&risl=&pid=ImgRaw&r=0' }}
//             className="w-full rounded-3xl shadow-xl"
//             style={{ height: carImageHeight }}
//             resizeMode="cover"
//           />
//         </View>
        
//         {/* Metrics */}
//         <View className="flex-row mt-6 px-4">
//           {/* RPM Metric */}
//           <View className="flex-1 bg-[#ffab76] p-4 rounded-xl mr-2 relative">
//             <View className="flex-row items-center">
//               <Image
//                 source={rpm}
//                 className="w-9 h-7 mr-2 text-white"
//               />
//               <Text className="text-base text-white font-bold">RPM</Text>
//             </View>
//             <View className="flex-row items-baseline mt-2">
//               <Text className="text-2xl font-bold text-gray-800">1173.5</Text>
//               <Text className="text-xs text-gray-600 ml-1 z-10">rpm</Text>
//             </View>
//             <Image
//               source={rpm2}
//               className="w-28 h-24 absolute -right-5 -bottom-2.5 text-white opacity-50 z-0"
//             />
//           </View>
          
//           {/* Speed Metric */}
//           <View className="flex-1 bg-[#93c6e7] p-4 rounded-xl ml-2 relative">
//             <View className="flex-row items-center">
//               <Image
//                 source={speed}
//                 className="w-9 h-7 mr-2 text-white"
//               />
//               <Text className="text-base text-white font-bold">Speed</Text>
//             </View>
//             <View className="flex-row items-baseline mt-2 relative">
//               <Text className="text-2xl font-bold text-gray-800">26</Text>
//               <Text className="text-xs text-gray-600 ml-1 z-10">km/h</Text>
//               <Image
//                 source={speed2}
//                 className="w-24 h-24 absolute -right-5 -bottom-7 text-white opacity-50 z-0"
//               />
//             </View>
//           </View>
//         </View>
        
//         {/* Features Label */}
//         <Text className="text-lg font-bold text-[#105e62] mt-4 mb-3 px-4">
//           Features
//         </Text>
        
//         {/* Features Grid - With responsive height */}
//         <View className="flex-row flex-wrap px-3">
//           {/* Car Log */}
//           <TouchableOpacity className="w-1/2 px-1 mb-2">
//             <View className="bg-[#e9e58f] rounded-xl p-4 justify-between relative"
//                  style={{ height: featureCardHeight }}>
//               <Text className="text-xl font-bold text-gray-800 z-10">Car Log</Text>
//               <Image
//                 source={car}
//                 className="w-10 h-12 self-end"
//               />
//               <Image
//                 source={curv}
//                 className="w-36 h-40 absolute -left-2 -top-1 text-white opacity-30 z-0"
//               />
//             </View>
//           </TouchableOpacity>
          
//           {/* Temperatures */}
//           <TouchableOpacity className="w-1/2 px-1 mb-2">
//             <View className="bg-[#ffab76] rounded-xl p-4 justify-between relative"
//                  style={{ height: featureCardHeight }}>
//               <Image
//                 source={temp1}
//                 className="w-36 h-40 absolute -right-5 -top-8 text-white opacity-20 z-0"
//               />
//               <Text className="text-xl font-bold text-gray-800">Temperatures</Text>
//               <Image
//                 source={temp}
//                 className="w-8 h-14 self-end"
//               />
//             </View>
//           </TouchableOpacity>
          
//           {/* Car Profile */}
//           <TouchableOpacity className="w-1/2 px-1 mb-2">
//             <View className="bg-[#93c6e7] rounded-xl p-4 justify-between"
//                  style={{ height: featureCardHeight }}>
//               <Text className="text-xl font-bold text-gray-800">Car Profile</Text>
//               <Image
//                 source={icon}
//                 className="w-16 h-12 self-end"
//               />
//             </View>
//           </TouchableOpacity>
          
//           {/* Locations */}
//           <TouchableOpacity 
//             className="w-1/2 px-1 mb-2 ml-auto" 
//             onPress={() => router.push('../maps/1')}
//           >
//             <View className="bg-[#badc58] rounded-xl p-4 justify-between relative"
//                  style={{ height: featureCardHeight }}>
//               <Image
//                 source={route}
//                 className="w-40 h-40 absolute -left-1 -bottom-2.5 opacity-70 z-0"
//               />
//               <Text className="text-xl font-bold text-gray-800 z-10">Locations</Text>
//               <Image
//                 source={location}
//                 className="w-16 h-16 self-end bg-white rounded-full z-10"
//               />
//             </View>
//           </TouchableOpacity>
//         </View>
        
//         {/* Added bottom padding for scrolling comfort */}
//         <View className="h-4" />
//       </ScrollView>
//     </SafeAreaView>
//   );
// }


// import React from 'react';
// import { Image, Text, View, StatusBar, ScrollView, TouchableOpacity } from 'react-native';
// import { Ionicons,MaterialCommunityIcons,FontAwesome, Feather } from '@expo/vector-icons';
// import { SafeAreaView } from 'react-native-safe-area-context';
// import { useAuth } from '@/providers/AuthProvider';
// import { Link, router, useRouter } from 'expo-router';

// export default function Home() {
//   const {user} = useAuth();
//   let currentDate = new Date();
//   return (
//     <>
//       <StatusBar
//         backgroundColor="#f4f1de"
//         barStyle="dark-content"  // This makes status bar elements black
//       />
//       <SafeAreaView className="flex-1">
//         <ScrollView className="bg-[#f4f1de] px-5 flex-1">
//           {/* Header Section */}
//           <View className="flex flex-row items-center mt-5 mb-5">
//             <Image
//               source={require('../../assets/images/profile.jpeg')}
//               className="w-10 h-10 rounded-full mr-2"
//             />
//             <View>
//               <Text className="text-lg font-bold text-black">Hello, {user?.name}</Text>
//                 <Text className="text-sm text-gray-600">
//                 {currentDate.toLocaleDateString('en-GB', {
//                   day: '2-digit',
//                   month: 'short',
//                   year: 'numeric',
//                 })}
//                 </Text>
//             </View>
//             {/* <TouchableOpacity className='ml-auto'>
//               <Ionicons name="search" size={24} color="black" />
//             </TouchableOpacity> */}
//             {/* <Link href="../maps/1">maps</Link> */}
//             <TouchableOpacity className='ml-auto' onPress={() => router.push('../maps/1')}>
//               <Feather name="map-pin" size={24} color="black" />
//             </TouchableOpacity>
//           </View>

//           {/* Daily Challenge Section */}
//           <View className="bg-[#e5d0ff] rounded-xl p-5 mb-5">
//             <Text className="text-2xl font-bold text-black">Daily challenge</Text>
//             <Text className="text-lg text-gray-600 my-2">Do your plan before 09:00 AM</Text>
//             <View className="flex flex-row items-center">
//               <Image
//                 source={require('../../assets/images/engine.jpg')} // Replace with avatar image URL
//                 className="w-10 h-10 rounded-full mr-1"
//               />
//               <Image
//                 source={require('../../assets/images/engine.jpg')} // Replace with avatar image URL
//                 className="w-10 h-10 rounded-full mr-1"
//               />
//               <Image
//                 source={require('../../assets/images/engine.jpg')} // Replace with avatar image URL
//                 className="w-10 h-10 rounded-full mr-1"
//               />
//               <Text className="text-lg font-bold text-gray-600">+4</Text>
//             </View>
//           </View>

//           {/* Date Picker Section */}
//           <View className="flex flex-row justify-between mb-5">
//             {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day, index) => (
//               <View
//                 key={index}
//                 className={`flex flex-col items-center py-2 ${day === 'Wed' ? 'bg-black rounded-full px-3' : ''}`}
//               >
//                 <Text
//                   className={`text-sm ${day === 'Wed' ? 'text-white' : 'text-gray-600'}`}
//                 >
//                   {day[0]}
//                 </Text>
//                 <Text
//                   className={`text-lg ${day === 'Wed' ? 'text-white' : 'text-gray-600'}`}
//                 >
//                   {23 + index}
//                 </Text>
//               </View>
//             ))}
//           </View>

//             {/* Your Car Status Section */}
//             <View className="mb-5">
//               <Text className="text-2xl font-bold text-black mb-3">Car status</Text>
//               <View className="flex flex-row justify-between">
//               {/* RPM Card */}
//               <View className="w-[48%] bg-[#ffdeaf] rounded-xl p-6">
//               <View className="flex flex-row items-center mb-2">
//               <MaterialCommunityIcons name="speedometer" size={24} color="black" />
//               <Text className="text-lg font-bold ml-2">RPM</Text>
//               </View>
//               <Text className="text-xl text-black mb-2">3000</Text>
//               <Text className="text-md text-gray-600">Timestamp: 25 Nov. 14:00</Text>
//               </View>
//               {/* Coolant Temp Card */}
//               <View className="w-[48%] bg-[#d0f4ff] rounded-xl p-6">
//               <View className="flex flex-row items-center mb-2">
//               <FontAwesome name="thermometer-4" size={24} color="black" />
//               <Text className="text-lg font-bold ml-2">Coolant Temp</Text>
//               </View>
//               <Text className="text-xl text-black mb-2">90°C</Text>
//               <Text className="text-md text-gray-600">Timestamp: 28 Nov. 18:00</Text>
//               </View>
//               </View>
//             </View>

//         </ScrollView>
//       </SafeAreaView>
    
//     </>
//   );
// }
