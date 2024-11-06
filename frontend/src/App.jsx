import { useState } from 'react';
import { Box, VStack, Input, Button } from '@chakra-ui/react';
import { ChatMessage } from './components/ChatMessage';
import { sendMessage } from './services/api';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSend = async () => {
    if (!input.trim()) return;

    setMessages(prev => [...prev, { text: input, isUser: true }]);
    setInput('');

    try {
      const response = await sendMessage(input);
      setMessages(prev => [...prev, { text: response.answer, isUser: false }]);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <Box maxW="800px" mx="auto" p={4}>
      <VStack spacing={4} h="80vh">
        <Box flex={1} w="100%" overflowY="auto">
          {messages.map((msg, i) => (
            <ChatMessage key={i} message={msg.text} isUser={msg.isUser} />
          ))}
        </Box>
        <Box w="100%">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask Pep about tactics..."
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          />
          <Button onClick={handleSend} ml={2}>
            Send
          </Button>
        </Box>
      </VStack>
    </Box>
  );
}

export default App;