import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import * as React from 'react';
import { AsyncStorage } from 'react-native';
import TabBarIcon from '../components/TabBarIcon';
import ve from '../screens/HomeScreen';
import LinksScreen from '../screens/LinksScreen';
import Login from '../components/Login';
import Register from '../components/Register';
import Record from '../components/Record';
import HomeScreen from '../screens/HomeScreen';

const BottomTab = createBottomTabNavigator();
const INITIAL_ROUTE_NAME = 'Home';

export default function BottomTabNavigator({ navigation, route }) {
  // Set the header title on the parent stack navigator depending on the
  // currently active tab. Learn more in the documentation:
  // https://reactnavigation.org/docs/en/screen-options-resolution.html
  navigation.setOptions({ headerTitle: getHeaderTitle(route) });

  return (
    <BottomTab.Navigator initialRouteName={INITIAL_ROUTE_NAME}>
      <BottomTab.Screen
        name='Map'
        component={HomeScreen}
        options={{
          title: 'Map',
        }}
      />
      <BottomTab.Screen
        name='Record'
        component={Record}
        options={{
          title: 'Record',
        }}
      />
      <BottomTab.Screen
        name='Login'
        component={Login}
        options={{
          title: 'Login',
        }}
      />
      <BottomTab.Screen
        name='Register'
        component={Register}
        options={{
          title: 'Register',
        }}
      />
    </BottomTab.Navigator>
  );
}

function getHeaderTitle(route) {
  const routeName =
    route.state?.routes[route.state.index]?.name ?? INITIAL_ROUTE_NAME;

  switch (routeName) {
    case 'Home':
      return 'Current map';
    case 'Links':
      return 'Links to learn more';
  }
}
