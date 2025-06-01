
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { Box, Text } from '@chakra-ui/react';
import { AuthProvider } from './contexts/AuthContext';
import Login from './features/auth/Login';
import Navbar from './components/Navbar';
import PrivateRoute from './components/PrivateRoute';

// Simple page components
const Dashboard = () => (
  <Box p={4}>
    <Text fontSize="2xl">Dashboard</Text>
  </Box>
);

const Orders = () => (
  <Box p={4}>
    <Text fontSize="2xl">Orders</Text>
  </Box>
);

const Positions = () => (
  <Box p={4}>
    <Text fontSize="2xl">Positions</Text>
  </Box>
);

const Profile = () => (
  <Box p={4}>
    <Text fontSize="2xl">Profile</Text>
  </Box>
);

// Main App Component
function App() {
  const queryClient = new QueryClient();

  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Router>
          <Box p={4} minH="100vh" bg="gray.50">
            <Navbar />
            <Box mt={4}>
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/" element={
                  <PrivateRoute>
                    <Dashboard />
                  </PrivateRoute>
                } />
                <Route path="/orders" element={
                  <PrivateRoute>
                    <Orders />
                  </PrivateRoute>
                } />
                <Route path="/positions" element={
                  <PrivateRoute>
                    <Positions />
                  </PrivateRoute>
                } />
                <Route path="/profile" element={
                  <PrivateRoute>
                    <Profile />
                  </PrivateRoute>
                } />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </Box>
          </Box>
        </Router>
        <ReactQueryDevtools initialIsOpen={false} />
      </AuthProvider>
    </QueryClientProvider>
  );
};

export default App;
