import React, { Component } from 'react';
import {
  Alert,
  AsyncStorage,
  Button,
  TextInput,
  Text,
  View,
  StyleSheet,
} from 'react-native';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#ecf0f1',
  },
  input: {
    width: 200,
    height: 44,
    padding: 10,
    borderWidth: 1,
    borderColor: 'black',
    marginBottom: 10,
  },
});

export default class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      username: 'username',
      password: 'password',
      token: '',
      data: null,
      error: null,
    };
  }

  onLogin() {
    fetch('http://192.168.0.111:5000/api/login', {
      method: 'post',
      mode: 'no-cors',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
        email: this.state.username,
        password: this.state.password,
      }),
    })
      .then((resp) => resp.json())
      .then((data) => {
        try {
          Alert.alert(data.message);
          AsyncStorage.setItem('userToken', data.token);
          AsyncStorage.setItem('loggedIn', 'true');
        } catch (error) {
          Alert.alert(error.error);
          console.log(error);
        }
      });
  }

  render() {
    return (
      <View style={styles.container}>
        <TextInput
          value={this.state.username}
          onChangeText={(username) => this.setState({ username })}
          placeholder={'Username'}
          style={styles.input}
        />
        <TextInput
          value={this.state.password}
          onChangeText={(password) => this.setState({ password })}
          placeholder={'Password'}
          secureTextEntry={true}
          style={styles.input}
        />
        <Button
          title={'LoginTest'}
          style={styles.input}
          onPress={this.onLogin.bind(this)}
        />
      </View>
    );
  }
}
