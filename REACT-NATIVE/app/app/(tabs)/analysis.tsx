import { View, Text, TouchableOpacity, ScrollView } from 'react-native'
import React from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'
import { MaterialCommunityIcons, FontAwesome5, FontAwesome6, FontAwesome } from '@expo/vector-icons'
import cardData from '../../constants/cardData'

const Analysis = () => {
  return (
    <SafeAreaView className="flex-1 bg-[#f1f4de]">
      <ScrollView>
        <View className='flex-1 p-12 bg-[#f1f4de] gap-6'>
        
          <View  className={`bg-[#C4E3FA] rounded-2xl shadow-md p-7 relative`}>
            <View className={`absolute -top-4 -left-4 bg-[#54B0E3] rounded-full p-4 shadow-md`}>                
                <MaterialCommunityIcons name='engine' size={32} color="#000000" />
            </View>
            <Text className="text-base font-bold mb-16 ml-8 text-black">
            Engine Health Monitoring
            </Text>
            <TouchableOpacity className={`self-end bg-[#54B0E3] rounded-full p-3`}>
              <FontAwesome6 name="searchengin" size={26} color="#000000" />
            </TouchableOpacity>
          </View>

          <View  className={`bg-[#A8E7E3] rounded-2xl shadow-md p-7 relative`}>
            <View className={`absolute -top-4 -left-4 bg-[#39C1C5] rounded-full p-4 shadow-md`}>                
                <FontAwesome5 name='shipping-fast' size={32} color="#000000" />
            </View>
            <Text className="text-base font-bold mb-16 ml-8 text-black">
            Emission Compliance
                        </Text>
            <TouchableOpacity className={`self-end bg-[#39C1C5] rounded-full p-3`}>
              <FontAwesome6 name="searchengin" size={26} color="#000000" />
            </TouchableOpacity>
          </View>

          <View  className={`bg-[#F5A982] rounded-2xl shadow-md p-7 relative`}>
            <View className={`absolute -top-4 -left-4 bg-[#E68050] rounded-full p-4 shadow-md`}>                
                <FontAwesome name='car' size={32} color="#000000" />
            </View>
            <Text className="text-base font-bold mb-16 ml-8 text-black">
            Driving Behavior Analysis
            </Text>
            <TouchableOpacity className={`self-end bg-[#E68050] rounded-full p-3`}>
              <FontAwesome6 name="searchengin" size={26} color="#000000" />
            </TouchableOpacity>
          </View>

          <View  className={`bg-[#EEE79D] rounded-2xl shadow-md p-7 relative`}>
            <View className={`absolute -top-4 -left-4 bg-[#DAC912] rounded-full p-4 shadow-md`}>                
                <FontAwesome5 name='tools' size={32} color="#000000" />
            </View>
            <Text className="text-base font-bold mb-16 ml-8 text-black">
            Predictive Maintenance
            </Text>
            <TouchableOpacity className={`self-end bg-[#DAC912] rounded-full p-3`}>
              <FontAwesome6 name="searchengin" size={26} color="#000000" />
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  )
}

export default Analysis
