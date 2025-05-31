import React, { createContext, useContext, useState } from 'react';
import { ChakraProvider, Box, Button, Text } from '@chakra-ui/react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

type ReactNode = React.ReactNode;

// Types
interface AuthContextType {
  isAuthenticated: boolean;
  login: () => void;
  logout: () => void;
}

// Create context with default value
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Auth Provider Component
const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  
  const login = () => setIsAuthenticated(true);
  const logout = () => setIsAuthenticated(false);

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook for using auth context
const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Simple page components
const Login = () => {
  const { login } = useAuth();
  return (
    <Box p={8}>
      <Box mb={4}>
        <Text fontSize="2xl">Login Page</Text>
      </Box>
      <Button colorScheme="blue" onClick={login}>
        Sign In
      </Button>
    </Box>
  );
};

const Dashboard = () => (
  <Box p={8}>
    <Text fontSize="2xl" mb={4}>Dashboard</Text>
    <Text>Welcome to your dashboard!</Text>
  </Box>
);

const Orders = () => (
  <Box p={8}>
    <Text fontSize="2xl" mb={4}>Orders</Text>
    <Text>Your orders will appear here</Text>
  </Box>
);

const Positions = () => (
  <Box p={8}>
    <Text fontSize="2xl" mb={4}>Positions</Text>
    <Text>Your positions will appear here</Text>
  </Box>
);

const Profile = () => (
  <Box p={8}>
    <Text fontSize="2xl" mb={4}>Profile</Text>
    <Text>Your profile information will appear here</Text>
  </Box>
);

// Navbar Component
const Navbar = () => {
  const { isAuthenticated, logout } = useAuth();
  
  if (!isAuthenticated) return null;
  
  return (
    <Box bg="blue.600" color="white" p={4} position="fixed" w="100%" top={0} zIndex={10}>
      <Text as="h1" fontSize="xl" fontWeight="bold" display="inline-block">
        Kite Trading
      </Text>
      <Button 
        onClick={logout} 
        size="sm" 
        colorScheme="red" 
        position="absolute" 
        right={4} 
        top={3}
      >
        Logout
      </Button>
    </Box>
  );
};

// Private Route Component
const PrivateRoute: React.FC<{ children: ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />;
};

// Main App Component
const App: React.FC = () => {
  const queryClient = new QueryClient();

  return (
    <ChakraProvider theme={theme} resetCSS>
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <Router>
            <Box p={4} minH="100vh" bg="gray.50">
              <Navbar />
              <Box mt={4}>
                <Routes>
                  <Route path="/login" element={<Login />} />
                  <Route
                    path="/"
                    element={
                      <PrivateRoute>
                        <Dashboard />
                      </PrivateRoute>
                    }
                  />
                  <Route
                    path="/orders"
                    element={
                      <PrivateRoute>
                        <Orders />
                      </PrivateRoute>
                    }
                  />
                  <Route
                    path="/positions"
                    element={
                      <PrivateRoute>
                        <Positions />
                      </PrivateRoute>
                    }
                  />
                  <Route
                    path="/profile"
                    element={
                      <PrivateRoute>
                        <Profile />
                      </PrivateRoute>
                    }
                  />
                  <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
              </Box>
            </Box>
          </Router>
          <ReactQueryDevtools initialIsOpen={false} />
        </AuthProvider>
      </QueryClientProvider>
    </ChakraProvider>
  );
};

export default App;
