import { Stack } from "expo-router";

export default function ProfileLayout(){
    return (
        <Stack>
            <Stack.Screen name="index" options={{headerShown: false, title: "Profile"}} />
            <Stack.Screen name="editProfile" options={{headerShown: true, title: "Edit", headerBackTitle: "Back"}} />
            <Stack.Screen name="licence" options={{headerShown: true, title: "Licence"}} />
            <Stack.Screen name="insurance" options={{headerShown: true, title: "Insurance"}} />
            <Stack.Screen name="puc" options={{headerShown: true, title: "Puc"}} />
            <Stack.Screen name="id-proof" options={{headerShown: true, title: "ID Proof"}} />
        </Stack>
    )
}