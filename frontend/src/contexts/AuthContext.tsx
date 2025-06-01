import { createContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

interface User {
  id: string;
  email: string;
  name: string;
}

interface AuthContextType {
  user: User | null;
  login: (email: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const fetchUser = async () => {
    try {
      // In a real app, you would fetch the user data from your backend
      // const response = await api.get('/users/me');
      // setUser(response.data);
      
      // Mock response for now
      const mockUser = { 
        id: '1', 
        email: 'user@example.com', 
        name: 'Test User' 
      };
      setUser(mockUser);
      return mockUser;
    } catch (error) {
      console.error('Failed to fetch user', error);
      localStorage.removeItem('access_token');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string) => {
    try {
      // In a real app, you would make an API call to your backend
      // const response = await api.post('/auth/login', { email, password });
      // const { user, token } = response.data;
      
      // Mock response for now
      const mockUser = { 
        id: '1', 
        email, 
        name: 'Test User' 
      };
      const mockToken = 'mock-jwt-token';
      
      localStorage.setItem('access_token', mockToken);
      setUser(mockUser);
      navigate('/dashboard');
    } catch (error) {
      console.error('Login failed', error);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
    navigate('/login');
  };

  // Check if user is already logged in on initial load
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (token) {
          // Here you would typically validate the token with your backend
          // and fetch the user data
          api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          await fetchUser();
        }
      } catch (error) {
        console.error('Failed to check authentication status', error);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const value: AuthContextType = {
    user,
    login,
    logout,
    isAuthenticated: !!user,
    loading,
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
