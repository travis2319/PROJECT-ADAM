import { Tabs } from 'expo-router';
import React from 'react';
import { Ionicons } from "@expo/vector-icons";

export default function TabLayout() {
  

  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: "#ffff",
        headerShown: false,
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: "Home",
          tabBarIcon: ({ focused }) => (
            <Ionicons
              name={focused ? "home-sharp" : "home-outline"}
              size={24}
              color="white"
            />
          ),
        }}
      />
      <Tabs.Screen
        name="explore"
        options={{
          title: "Home",
          tabBarIcon: ({ focused }) => (
            <Ionicons
              name={focused ? "search" : "search-outline"}
              size={24}
              color="white"
            />
          ),
        }}
      />
    </Tabs>
  );
}
