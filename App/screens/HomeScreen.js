import React, { Component } from 'react';
import { Text, View, AsyncStorage } from 'react-native';
import MapView from 'react-native-maps';
import * as Permissions from 'expo-permissions';
import * as Location from 'expo-location';
import { Audio } from 'expo-av';

export default class HomeScreen extends Component {
  constructor(props) {
    super(props);

    this.state = {
      latitude: null,
      longitude: null,
      isLogged: 'false',
    };
  }

  async componentDidMount() {
    const { status } = await Permissions.getAsync(Permissions.LOCATION);

    if (status !== 'granted') {
      const response = await Permissions.askAsync(Permissions.LOCATION);
    }

    let location = await Location.getCurrentPositionAsync({});
    let userToken = await AsyncStorage.getItem('userToken');
    let isLogged = await AsyncStorage.getItem('loggedIn');

    console.log(userToken);

    let placeName = await Location.reverseGeocodeAsync({
      latitude: location.coords.latitude,
      longitude: location.coords.longitude,
    });

    console.log(`Current place name is: ${placeName[0].name}`);

    fetch('http://192.168.0.111:5000/api/set_location', {
      method: 'post',
      mode: 'no-cors',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
        data: {
          lat: location.coords.latitude,
          lon: location.coords.longitude,
          place_name: placeName[0].name,
        },
        token: userToken,
      }),
    })
      .then((resp) => resp.json())
      .then((data) => {
        try {
          console.log('Map data return: ');
          console.log(data);
        } catch (err) {
          console.log(err);
        }
      });
    this.setState({
      latitude: location.coords.latitude,
      longitude: location.coords.longitude,
      isLogged,
    });
  }

  render() {
    const { latitude, longitude, isLogged } = this.state;

    if (latitude && isLogged === 'true') {
      return (
        <MapView
          style={{ flex: 1 }}
          initialRegion={{
            latitude,
            longitude,
            latitudeDelta: 0.0922,
            longitudeDelta: 0.0421,
          }}
        />
      );
    } else {
      return (
        <View>
          <Text>
            Either there is no latitude found, or you haven't logged in yet
          </Text>
        </View>
      );
    }
  }
}
