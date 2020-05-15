import React, { Component } from 'react';
import { Alert, Button, TextInput, Text, View, StyleSheet } from 'react-native';

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
      confirmPassword: '',
      hashedPassword: '',
    };
  }

  onRegister() {
    const { username, password } = this.state;
    try {
      fetch('/api/register', {
        method: 'post',
        mode: 'no-cors',
        headers: {
          'Content-type': 'application/json',
        },
        body: JSON.stringify({
          email: username,
          password: password,
        }),
      });
    } catch (error) {
      console.log(error);
    }
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
        <TextInput
          value={this.state.confirmPassword}
          onChangeText={(confirmPassword) => this.setState({ confirmPassword })}
          placeholder={'Confirm Password'}
          secureTextEntry={true}
          style={styles.input}
        />
        <Button
          title={'Register'}
          style={styles.input}
          disabled={
            this.state.username
              ? this.state.password === this.state.confirmPassword
                ? false
                : true
              : true
          }
          onPress={this.onRegister.bind(this)}
        />
      </View>
    );
  }
}
