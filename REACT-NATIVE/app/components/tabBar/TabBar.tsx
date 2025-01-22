import { View } from 'react-native';
import { useLinkBuilder, useTheme } from '@react-navigation/native';
import { PlatformPressable } from '@react-navigation/elements';
import { BottomTabBarProps } from '@react-navigation/bottom-tabs';
import { Feather , FontAwesome5,Entypo} from '@expo/vector-icons';

export default function TabBar({ state, descriptors, navigation }: BottomTabBarProps) {
  const { buildHref } = useLinkBuilder();
  
  const icon: { [key: string]: (props: any) => JSX.Element } = {
    index: (props: any) => <Feather name='home' size={24} color={props.color} />,
    analysis: (props: any) => <FontAwesome5 name='robot' size={24} color={props.color} />,
    chat: (props: any) => <Feather name='message-square' size={24} color={props.color} />,
    profile: (props: any) => <Feather name='user' size={24} color={props.color} />,
  }

  return (
    <View className="absolute bottom-6 flex-row justify-between items-center bg-[#14213d] mx-20 py-4 rounded-full shadow-md">
      {state.routes.map((route, index) => {
        const { options } = descriptors[route.key];
        const isFocused = state.index === index;

        const onPress = () => {
          const event = navigation.emit({
            type: 'tabPress',
            target: route.key,
            canPreventDefault: true,
          });

          if (!isFocused && !event.defaultPrevented) {
            navigation.navigate(route.name, route.params);
          }
        };

        const onLongPress = () => {
          navigation.emit({
            type: 'tabLongPress',
            target: route.key,
          });
        };

        return (
          <PlatformPressable
            key={route.key}
            href={buildHref(route.name, route.params)}
            accessibilityState={isFocused ? { selected: true } : {}}
            accessibilityLabel={options.tabBarAccessibilityLabel}
            testID={options.tabBarButtonTestID}
            onPress={onPress}
            onLongPress={onLongPress}
            className="flex-1 justify-center items-center"
          >
            {icon[route.name]?.({
              color: isFocused ? "#ffffff" : "#ffffff80",
            })}
          </PlatformPressable>
        );
      })}
    </View>
  );
}

// import { View, Platform } from 'react-native';
// import { useLinkBuilder, useTheme } from '@react-navigation/native';
// import { Text, PlatformPressable } from '@react-navigation/elements';
// import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

// import { BottomTabBarProps } from '@react-navigation/bottom-tabs';
// import { Feather } from '@expo/vector-icons';

// export default function TabBar({ state, descriptors, navigation }: BottomTabBarProps) {
//   const { colors } = useTheme();
//   const { buildHref } = useLinkBuilder();
//   const icon: { [key: string]: (props: any) => JSX.Element } = {
//     index: (props: any) => <Feather name='home' size={24} color={props.color}/>,
//     explore: (props: any) => <Feather name='compass' size={24} color={props.color} />,
//   }
//   return (
//     <View className="absolute bottom-6 flex-row justify-between items-center bg-[#00171f] mx-20 py-4 rounded-full shadow-md">
//   {state.routes.map((route, index) => {
//     const { options } = descriptors[route.key];
//     const label =
//       options.tabBarLabel !== undefined
//         ? options.tabBarLabel
//         : options.title !== undefined
//           ? options.title
//           : route.name;

//     const isFocused = state.index === index;

//     const onPress = () => {
//       const event = navigation.emit({
//         type: 'tabPress',
//         target: route.key,
//         canPreventDefault: true,
//       });

//       if (!isFocused && !event.defaultPrevented) {
//         navigation.navigate(route.name, route.params);
//       }
//     };

//     const onLongPress = () => {
//       navigation.emit({
//         type: 'tabLongPress',
//         target: route.key,
//       });
//     };

//     return (
//       <PlatformPressable
//         key={route.key}
//         href={buildHref(route.name, route.params)}
//         accessibilityState={isFocused ? { selected: true } : {}}
//         accessibilityLabel={options.tabBarAccessibilityLabel}
//         testID={options.tabBarButtonTestID}
//         onPress={onPress}
//         onLongPress={onLongPress}
//         className="flex-1 justify-center items-center space-y-1"
//       >
//         {icon[route.name]?.({
//             color: isFocused ? "#673ab7" : "#fff",
//         })}
//         <Text
//           style={{
//             color: isFocused ? colors.primary : colors.text,
//           }}
//           className={`${isFocused ? "text-primary" : "text-base-content"}`}
//         >
//            {typeof label === 'function'
//                 ? label({
//                     focused: isFocused,
//                     color: isFocused ? "#ffffff" : "#ffffff80",
//                     position: 'below-icon',
//                     children: '',
//                   })
//                 : label}
//         </Text>
//       </PlatformPressable>
//     );
//   })}
// </View>

//   );
// }



// <View style={{ position: 'absolute', bottom: 25, flexDirection: 'row',justifyContent:'space-between',alignContent:'center',backgroundColor:'#fff',marginHorizontal:80,paddingVertical:15,borderRadius:35,shadowColor:'#fff',shadowOffset:{width:0,height:10},shadowOpacity:0.25,shadowRadius:10,elevation:0.1 }}>
    //   {state.routes.map((route, index) => {
    //     const { options } = descriptors[route.key];
    //     const label =
    //       options.tabBarLabel !== undefined
    //         ? options.tabBarLabel
    //         : options.title !== undefined
    //           ? options.title
    //           : route.name;

    //     const isFocused = state.index === index;

    //     const onPress = () => {
    //       const event = navigation.emit({
    //         type: 'tabPress',
    //         target: route.key,
    //         canPreventDefault: true,
    //       });

    //       if (!isFocused && !event.defaultPrevented) {
    //         navigation.navigate(route.name, route.params);
    //       }
    //     };

    //     const onLongPress = () => {
    //       navigation.emit({
    //         type: 'tabLongPress',
    //         target: route.key,
    //       });
    //     };

    //     return (
    //       <PlatformPressable
    //         key={route.key}
    //         href={buildHref(route.name, route.params)}
    //         accessibilityState={isFocused ? { selected: true } : {}}
    //         accessibilityLabel={options.tabBarAccessibilityLabel}
    //         testID={options.tabBarButtonTestID}
    //         onPress={onPress}
    //         onLongPress={onLongPress}
    //         style={{ flex: 1,justifyContent:'center', alignItems:'center',gap:5
    //          }}
    //       >
    //         <Text style={{ color: isFocused ? colors.primary : colors.text }}>
    //           {typeof label === 'function' ? label({ focused: isFocused, color: isFocused ? colors.primary : colors.text, position: 'below-icon', children: '' }) : label}
    //         </Text>
    //       </PlatformPressable>
    //     );
    //   })}
    // </View>