// constants/homeData.ts
import car from "@/assets/images/carlog.png";
import temp from "@/assets/images/temp.png";
import temp1 from "@/assets/images/temp1.png";
import icon from "@/assets/images/prof.png";
import location from "@/assets/images/loc.png";
import curv from "@/assets/images/curv.png";
import route from "@/assets/images/route.png";
import { FeatureType } from '@/types/features';

export const FEATURES_DATA: FeatureType[] = [
  {
    title: 'Car Log',
    icon: car,
    backgroundIcon: curv,
    backgroundColor: '#e9e58f',
    navigateTo: '',
  },
  {
    title: 'Temperatures',
    icon: temp,
    backgroundIcon: temp1,
    backgroundColor: '#ffab76',
    navigateTo: '',
  },
  {
    title: 'Car Profile',
    icon: icon,
    backgroundColor: '#93c6e7',
    navigateTo: '/(profile)',
  },
  {
    title: 'Locations',
    icon: location,
    backgroundIcon: route,
    backgroundColor: '#badc58',
    navigateTo: '../maps/1',
  },
];