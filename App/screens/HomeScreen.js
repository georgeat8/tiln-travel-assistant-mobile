import React, { Component } from 'react';
import { Text, View, AsyncStorage } from 'react-native';
import MapView from 'react-native-maps';

export default class HomeScreen extends Component {
  constructor(props) {
    super(props);

    this.state = {
      latitude: 0,
      longitude: 0,
      error: '',
    };
  }

  gatherLocations() {
    this.watchId = navigator.geolocation.watchPosition(
      (position) => {
        this.setState({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        });
      },
      (error) => {
        this.setState({
          error,
        });
      },
      { distanceFilter: 100 }
    );
  }

  sendDataToApi() {
    const userToken = AsyncStorage.getItem('userToken');
    this.gatherLocations();
    fetch('/api/set_location', {
      method: 'post',
      mode: 'no-cors',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
        lat: this.state.latitude,
        lon: this.state.longitude,
        date: Date.now(),
        user_token: userToken,
      }),
    });
  }

  render() {
    return <MapView />;
  }
}
