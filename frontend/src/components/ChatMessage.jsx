import { Box, Text } from '@chakra-ui/react';

export const ChatMessage = ({ message, isUser }) => (
  <Box
    bg={isUser ? 'blue.100' : 'gray.100'}
    p={3}
    borderRadius="lg"
    maxW="80%"
    ml={isUser ? 'auto' : 0}
  >
    <Text>{message}</Text>
  </Box>
);