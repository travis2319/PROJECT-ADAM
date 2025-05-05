import React, { useEffect, useRef, useState } from 'react';
import MapView, { Marker, PROVIDER_GOOGLE } from 'react-native-maps';
import { StyleSheet, TouchableOpacity, View, Text, Dimensions, FlatList } from 'react-native';
import * as Location from 'expo-location';

const { width, height } = Dimensions.get('window');
const CARD_WIDTH = width * 0.3;

interface Category {
    id: string;
    name: string;
}

interface LocationData {
    name: string;
    latitude: number;
    longitude: number;
}

const CATEGORIES: Category[] = [
    { id: 'petrol', name: 'Petrol Pump' },
    { id: 'service', name: 'Service Center' },
    { id: 'carwash', name: 'Car Wash' },
];

const LOCATIONS: Record<string, LocationData[]> = {
    petrol: [
        { name: "City Fuels & Service", latitude: 15.273918, longitude: 73.957442 },
        { name: "Highway Energy Station", latitude: 15.277022, longitude: 73.958448 },
        { name: "Metro Petroleum", latitude: 15.291839, longitude: 73.9761 },
    ],
    service: [
        { name: "AutoCare Spares", latitude: 15.273151, longitude: 73.980684 },
        { name: "Luxury Car Service", latitude: 15.269786, longitude: 73.983527 },
        { name: "Premium Auto Workshop", latitude: 15.267995, longitude: 73.961680 },
    ],
    carwash: [
        { name: "GSL Service Center", latitude: 15.264492, longitude: 73.976166 },
        { name: "Angle's Car Studio", latitude: 15.269147, longitude: 73.965574 },
        { name: "Express Car Spa", latitude: 15.272896, longitude: 73.971444 },
    ],
};

export default function Maps() {
    const mapRef = useRef<MapView | null>(null);
    const [selectedCategory, setSelectedCategory] = useState<string>('petrol');

    const requestLocationPermission = async () => {
        try {
            const { status } = await Location.requestForegroundPermissionsAsync();
            if (status !== 'granted') {
                console.log('Permission to access location was denied');
                return;
            }

            const location = await Location.getCurrentPositionAsync({});
            const currentRegion = {
                latitude: location.coords.latitude,
                longitude: location.coords.longitude,
                latitudeDelta: 0.05,
                longitudeDelta: 0.05,
            };
            mapRef.current?.animateToRegion(currentRegion, 1000);
        } catch (error) {
            console.log('Error getting location', error);
        }
    };

    useEffect(() => {
        requestLocationPermission();
    }, []);

    return (
        <View style={styles.container}>
            <MapView
                ref={mapRef}
                style={styles.map}
                provider={PROVIDER_GOOGLE}
                showsUserLocation
                showsMyLocationButton
            >
                {LOCATIONS[selectedCategory].map((marker, index) => (
                    <Marker 
                        key={index} 
                        coordinate={{ latitude: marker.latitude, longitude: marker.longitude }} 
                        title={marker.name} 
                    />
                ))}
            </MapView>
            
            <View style={styles.carouselContainer}>
                <FlatList
                    data={CATEGORIES}
                    horizontal
                    keyExtractor={(item) => item.id}
                    contentContainerStyle={styles.carousel}
                    renderItem={({ item }) => (
                        <TouchableOpacity
                            style={[styles.categoryButton, selectedCategory === item.id && styles.activeButton]}
                            onPress={() => setSelectedCategory(item.id)}
                        >
                            <Text style={[styles.buttonText, selectedCategory === item.id && styles.activeText]}>
                                {item.name}
                            </Text>
                        </TouchableOpacity>
                    )}
                />
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    map: {
        flex: 1,
    },
    carouselContainer: {
        position: 'absolute',
        bottom: 20,
        width: '100%',
    },
    carousel: {
        paddingHorizontal: 10,
    },
    categoryButton: {
        width: CARD_WIDTH,
        padding: 10,
        backgroundColor: '#fff',
        borderRadius: 10,
        alignItems: 'center',
        justifyContent: 'center',
        marginHorizontal: 5,
        elevation: 3,
    },
    activeButton: {
        backgroundColor: '#007AFF',
    },
    buttonText: {
        fontSize: 14,
        fontWeight: 'bold',
        color: '#000',
    },
    activeText: {
        color: '#fff',
    },
});


// import React, { lazy, useEffect, useRef, useState } from 'react';
// import MapView, { Marker, PROVIDER_GOOGLE } from 'react-native-maps';
// import { StyleSheet, TouchableOpacity, View, Text, Dimensions, FlatList, Modal, ScrollView } from 'react-native';
// import { useNavigation } from 'expo-router';
// import * as Location from 'expo-location';

// const { width, height } = Dimensions.get('window');
// const CARD_WIDTH = width * 0.8;
// const SPACING = width * 0.1;

// // Location Categories Data
// const PETRO_PUMP_LOCATIONS = [
//     { name: "City Fuels & Service",  latitude: 15.273918126593086, longitude: 73.95744219694588 ,latitudeDelta: 0.0922, longitudeDelta: 0.0421},
//     { name: "Highway Energy Station", latitude: 15.277022, longitude: 73.958448, latitudeDelta: 0.0922, longitudeDelta: 0.0421},
//     { name: "Metro Petroleum", latitude: 15.291839, longitude: 73.9761, latitudeDelta: 0.0922, longitudeDelta: 0.0421 },
// ];

// const SERVICE_CENTER_LOCATIONS = [
//     { name: "AutoCare spares and service", latitude: 15.273151710614384,  longitude: 73.98068481062148, latitudeDelta: 0.0922, longitudeDelta: 0.0421 },
//     { name: "Luxury Car Service",  latitude: 15.269786890815313,  longitude: 73.9835275934396, latitudeDelta: 0.0922, longitudeDelta: 0.0421 },
//     { name: "Premium Auto Workshop", latitude: 15.26799518224674,  longitude: 73.96168021118278, latitudeDelta: 0.0922, longitudeDelta: 0.0421 },
// ];

// const CAR_WASH_LOCATIONS = [
//     { name: "GSL service center,washing",  latitude: 15.264492041429683,  longitude: 73.97616661099481, latitudeDelta: 0.0922, longitudeDelta: 0.0421 },
//     { name: "Angle's Car Detailing studio",  latitude: 15.26914719530096,  longitude: 73.9655743313175, latitudeDelta: 0.0922, longitudeDelta: 0.0421 },
//     { name: "Express Car Spa", latitude: 15.272896056684857,  longitude: 73.97144488365855, latitudeDelta: 0.0922, longitudeDelta: 0.0421 },
// ];


// export default function Maps() {
//     // const navigation = useNavigation();
//     const mapRef = useRef<MapView>(null);
    

//     const requestLocationPermission = async () => {
//         try {
//             const { status } = await Location.requestForegroundPermissionsAsync();
//             if (status !== 'granted') {
//                 console.log('Permission to access location was denied');
//                 return;
//             }

//             const location = await Location.getCurrentPositionAsync({});
//             const currentRegion = {
//                 latitude: location.coords.latitude,
//                 longitude: location.coords.longitude,
//                 latitudeDelta: 0.0922,
//                 longitudeDelta: 0.0421,
//             };
//             mapRef.current?.animateToRegion(currentRegion, 1000);
//         } catch (error) {
//             console.log('Error getting location', error);
//         }
//     };

//     return (
//         <View style={styles.container}>
//             <MapView
//                 ref={mapRef}
//                 style={styles.map}
//                 provider={PROVIDER_GOOGLE}
//                 showsUserLocation
//                 showsMyLocationButton
//                 onMapReady={requestLocationPermission}
//             >
//                 {PETRO_PUMP_LOCATIONS.map((marker, index) => 
//                 <Marker key={index} coordinate={marker}/>    
//             )}
//             </MapView>
//         </View>
//     );
// }

// const styles = StyleSheet.create({
//     container: {
//         flex: 1,
//     },
//     map: {
//         width: '100%',
//         height: '100%',
//     },
//     carouselContainer: {
//         position: 'absolute',
//         bottom: 20,
//         width: '100%',
//     },
//     carousel: {
//         paddingHorizontal: SPACING / 2,
//     },
//     card: {
//         width: CARD_WIDTH,
//         marginHorizontal: SPACING / 2,
//         padding: 20,
//         borderRadius: 15,
//         backgroundColor: 'white',
//         shadowColor: '#000',
//         shadowOffset: {
//             width: 0,
//             height: 2,
//         },
//         shadowOpacity: 0.25,
//         shadowRadius: 3.84,
//         elevation: 5,
//     },
//     selectedCard: {
//         transform: [{ scale: 1.05 }],
//     },
//     cardTitle: {
//         fontSize: 18,
//         fontWeight: 'bold',
//         color: 'white',
//         marginBottom: 8,
//     },
//     cardCount: {
//         fontSize: 14,
//         color: 'white',
//     },
//     modalContainer: {
//         flex: 1,
//         justifyContent: 'center',
//         backgroundColor: 'rgba(0, 0, 0, 0.5)',
//     },
//     modalContent: {
//         backgroundColor: 'white',
//         marginHorizontal: 20,
//         borderRadius: 20,
//         maxHeight: height * 0.7,
//     },
//     modalHeader: {
//         flexDirection: 'row',
//         justifyContent: 'space-between',
//         alignItems: 'center',
//         padding: 15,
//         borderBottomWidth: 1,
//         borderBottomColor: '#eee',
//     },
//     modalTitle: {
//         fontSize: 18,
//         fontWeight: 'bold',
//     },
//     closeButton: {
//         color: '#FF6B6B',
//         fontSize: 16,
//     },
//     locationsList: {
//         padding: 10,
//     },
//     locationItem: {
//         padding: 15,
//         borderBottomWidth: 1,
//         borderBottomColor: '#eee',
//     },
//     locationName: {
//         fontSize: 16,
//         fontWeight: 'bold',
//         marginBottom: 5,
//     },
//     locationAddress: {
//         color: '#666',
//     },
// });

// import React, { useEffect, useRef } from 'react';
// import MapView, { Marker, PROVIDER_GOOGLE } from 'react-native-maps';
// import { StyleSheet, TouchableOpacity, View, Text } from 'react-native';
// import { useNavigation } from 'expo-router';
// import * as Location from 'expo-location';


// const MARKER_COORDINATE = {
//     latitude: 18.520430,
//     longitude: 73.856743,
// };

// export default function Maps() {
//     const navigation = useNavigation();
//     const mapRef = useRef<MapView>(null);

//     useEffect(() => {
//         navigation.setOptions({
//             headerTitle: 'Map',
//             headerRight: () => <TouchableOpacity onPress={focusMap} >
//                 <Text>Focus</Text>
//             </TouchableOpacity>,
//         });
//     }, []);

//     const focusMap = () => {
//         mapRef.current?.animateCamera(
//             { center: MARKER_COORDINATE, zoom: 10 }, 
//             { duration: 2000 });
//         console.log('pressed!!');
//     };

//     const requestLocationPermission = async () => {
//         try {
//             const { status } = await Location.requestForegroundPermissionsAsync();
//             if (status !== 'granted') {
//                 console.log('Permission to access location was denied');
//                 return;
//             }
            
//             const location = await Location.getCurrentPositionAsync({});
//             const currentRegion = {
//                 latitude: location.coords.latitude,
//                 longitude: location.coords.longitude,
//                 latitudeDelta: 0.0922,
//                 longitudeDelta: 0.0421,
//             };
//             mapRef.current?.animateToRegion(currentRegion, 1000);
//         } catch (error) {
//             console.log('Error getting location', error);
//         }
//     };

//     return (
//         <View style={styles.container}>
//             <MapView
//                 ref={mapRef}
//                 style={styles.map}
//                 provider={PROVIDER_GOOGLE}
//                 showsUserLocation
//                 showsMyLocationButton
//                 onMapReady={requestLocationPermission}
//             >
//                 <Marker coordinate={MARKER_COORDINATE} />
//             </MapView>
//         </View>
//     );
// }

// const styles = StyleSheet.create({
//     container: {
//         flex: 1,
//     },
//     map: {
//         width: '100%',
//         height: '100%',
//     },
// });
