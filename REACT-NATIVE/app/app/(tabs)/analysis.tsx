import { View, Text, TouchableOpacity, ScrollView } from 'react-native'
import React from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'
import { Ionicons,MaterialCommunityIcons,FontAwesome5,FontAwesome6,FontAwesome } from '@expo/vector-icons'
import cardData from '../../constants/cardData'

const Analysis = () => {
  return (
    <SafeAreaView className="flex-1 bg-[#f1f4de]">
      <ScrollView>
        <View className='flex-1 p-12 bg-[#f1f4de] gap-6'>
        {cardData.map((card, index) => (
          <View key={index} className={`bg-[${card.bgColor}] rounded-2xl shadow-md p-7 relative`}>
            <View className={`absolute -top-4 -left-4 bg-[${card.iconBgColor}] rounded-full p-4 shadow-md`}>
                  {card.titleIconType === 'Ionicons' ? (
                  <Ionicons name={card.titleIconName} size={32} color="#000000" />
                  ) : card.titleIconType === 'MaterialCommunityIcons' ? (
                  <MaterialCommunityIcons name={card.titleIconName} size={32} color="#000000" />
                  ) : card.titleIconType === 'FontAwesome' ? (
                  <FontAwesome name={card.titleIconName} size={32} color="#000000" />
                  ) : (
                  <FontAwesome5 name={card.titleIconName} size={32} color="#000000" />
                  )}
            </View>
            <Text className="text-base font-bold mb-16 ml-8 text-black">
              {card.title}
            </Text>
            <TouchableOpacity className={`self-end bg-[${card.iconBgColor}] rounded-full p-3`}>
              <FontAwesome6 name="searchengin" size={26} color="#000000" />
            </TouchableOpacity>
          </View>
        ))}
        </View>
      </ScrollView>
    </SafeAreaView>
  )
}

export default Analysis
