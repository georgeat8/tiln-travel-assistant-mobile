import React, { useState } from "react";
import { Text, Button, View, TextInput } from 'react-native';

export default function App() {
  const [showLogin, setShowLogin] = useState(false)
  const [showRegister, setShowRegister] = useState(false)

  const login = () => {
    setShowLogin(!showLogin);
  }
  const register = () => {
    setShowRegister(!showRegister);
  }
  return (
    <View>
      <Button
      onPress={() => {
        login();
      }}
      color="blue"
      title="LOGIN"
      />
        {showLogin && 
        <View>
          <Text>Login</Text>
          <TextInput
            style={{
              height: 40,
              borderColor: 'gray',
              borderWidth: 1
            }}
          defaultValue="Name"
          />
        </View>
       } 
      <Button
      onPress={() => {
        register();
      }}
      color="blue"
      title="REGISTER"
      />
        {showRegister && 
          <View>
           <Text>Register</Text>
            <TextInput
               style={{
                height: 40,
                borderColor: 'gray',
                borderWidth: 1
                }}
             defaultValue="Name"
            />
          </View>
        }
     </View>
  );


}






