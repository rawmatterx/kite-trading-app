import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  VStack,
  Heading,
  Text,
  useToast,
  Link as ChakraLink,
  InputGroup,
  InputRightElement,
  IconButton,
} from '@chakra-ui/react';
import { ViewIcon, ViewOffIcon } from '@chakra-ui/icons';
import { useAuth } from '../../contexts/AuthContext';
import { Link as RouterLink } from 'react-router-dom';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();
  const toast = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!email || !password) {
      toast({
        title: 'Error',
        description: 'Please fill in all fields',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }

    try {
      setIsLoading(true);
      await login(email, password);
      toast({
        title: 'Login successful',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      navigate('/');
    } catch (error: any) {
      console.error('Login error:', error);
      toast({
        title: 'Login failed',
        description: error.response?.data?.detail || 'An error occurred during login',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container 
      maxW="container.sm" 
      display="flex" 
      flexDirection="column" 
      justifyContent="center" 
      minH="100vh"
      p={4}
      bg="gray.50"
    >
      <Box 
        maxW="md" 
        mx="auto"
        p={8} 
        borderWidth={1} 
        borderRadius="lg" 
        boxShadow="lg" 
        bg="white"
      >
        <VStack spacing={6}>
          <Heading as="h1" size="xl" textAlign="center">Sign In</Heading>
          
          <Box as="form" onSubmit={handleSubmit} w="full">
            <VStack spacing={4}>
              <FormControl id="email" isRequired>
                <FormLabel>Email address</FormLabel>
                <Input 
                  type="email" 
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email"
                  autoComplete="email"
                />
              </FormControl>

              <FormControl id="password" isRequired>
                <FormLabel>Password</FormLabel>
                <InputGroup>
                  <Input
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter your password"
                    autoComplete="current-password"
                  />
                  <InputRightElement h="full">
                    <Button
                      variant="ghost"
                      onClick={() => setShowPassword(!showPassword)}
                      aria-label={showPassword ? 'Hide password' : 'Show password'}
                    >
                      {showPassword ? <ViewOffIcon /> : <ViewIcon />}
                    </Button>
                  </InputRightElement>
                </InputGroup>
              </FormControl>

              <Button
                type="submit"
                colorScheme="blue"
                isLoading={isLoading}
                loadingText="Signing in..."
                width="full"
                mt={4}
                size="lg"
              >
                Sign In
              </Button>
            </VStack>
          </Box>

          <Text textAlign="center">
            Don't have an account?{' '}
            <ChakraLink as={RouterLink} to="/register" color="blue.500" fontWeight="medium">
              Sign up
            </ChakraLink>
          </Text>
        </VStack>
      </Box>
    </Container>
  );
};

export default Login;
