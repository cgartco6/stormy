import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, StyleSheet, FlatList } from 'react-native';
import Voice from '@react-native-voice/voice';
import { io } from 'socket.io-client';

export default function App() {
  const [message, setMessage] = useState('');
  const [conversation, setConversation] = useState([]);
  const socket = io('http://localhost:5000'); // Connect to backend

  useEffect(() => {
    Voice.onSpeechResults = onSpeechResults;
    return () => Voice.destroy().then(Voice.removeAllListeners);
  }, []);

  const onSpeechResults = (e) => {
    setMessage(e.value[0]);
    sendMessage(e.value[0]);
  };

  const sendMessage = async (text) => {
    setConversation([...conversation, { from: 'user', text }]);
    // Send to backend
    const response = await fetch('http://localhost:5000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });
    const data = await response.json();
    setConversation(prev => [...prev, { from: 'stormy', text: data.reply }]);
  };

  const startListening = () => {
    Voice.start('en-US');
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={conversation}
        keyExtractor={(item, idx) => idx.toString()}
        renderItem={({ item }) => (
          <Text style={item.from === 'user' ? styles.userMsg : styles.stormyMsg}>
            {item.from === 'user' ? 'You: ' : 'Stormy: '}{item.text}
          </Text>
        )}
      />
      <TextInput
        style={styles.input}
        value={message}
        onChangeText={setMessage}
        onSubmitEditing={() => sendMessage(message)}
      />
      <Button title="🎤" onPress={startListening} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, justifyContent: 'flex-end' },
  input: { borderWidth: 1, borderColor: '#ccc', padding: 10, marginVertical: 10 },
  userMsg: { alignSelf: 'flex-end', backgroundColor: '#d1e7ff', padding: 8, marginVertical: 4, borderRadius: 8 },
  stormyMsg: { alignSelf: 'flex-start', backgroundColor: '#ffe0b5', padding: 8, marginVertical: 4, borderRadius: 8 }
});
