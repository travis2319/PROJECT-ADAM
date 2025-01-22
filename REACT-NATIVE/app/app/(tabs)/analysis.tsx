import { StyleSheet, View, Text, Image, Platform } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function Analysis() {
  const statusCards = [
    {
      title: 'Engine Health',
      status: 'done',
      statusColor: '#81B29A' // Green for done
    },
    {
      title: 'Exhaust Compliance',
      status: 'pending',
      statusColor: '#F2CC8F' // Yellow for pending
    },
    {
      title: 'Engine Diagnostic',
      status: 'computing',
      statusColor: '#E07A5F' // Red-orange for computing
    }
  ];

  return (
    <SafeAreaView>
      <View className="flex justify-center items-center min-h-screen bg-[#f4f1de] px-4">
        <Text className="text-4xl font-bold text-black mb-8">Analysis</Text>
        
        <View className="w-full max-w-md gap-4">
          {statusCards.map((card, index) => (
            <View 
              key={index} 
              className="bg-white rounded-xl p-4 shadow-md"
            >
              <View className="flex flex-row justify-between items-center">
                <Text className="text-xl font-semibold text-gray-800">
                  {card.title}
                </Text>
                <View 
                  className="px-3 py-1 rounded-full" 
                  style={{ backgroundColor: card.statusColor }}
                >
                  <Text className="text-white font-medium capitalize">
                    {card.status}
                  </Text>
                </View>
              </View>
            </View>
          ))}
        </View>
      </View>
    </SafeAreaView>
  );
}


// import { StyleSheet, View,Text,Image, Platform } from 'react-native';
// import { SafeAreaView } from 'react-native-safe-area-context';

// export default function Ai() {
//   return (
//     <SafeAreaView> 
//       <View className='flex justify-center items-center h-screen bg-[#f4f1de] '>
//         <Text className='text-4xl font-bold text-black'>AI</Text>
//       </View>
//     </SafeAreaView>
//   );
// }