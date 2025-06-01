import { Flex, Button, useColorMode, useColorModeValue, Box, Text } from '@chakra-ui/react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import { MoonIcon, SunIcon } from '@chakra-ui/icons';
import { useAuth } from '../hooks/useAuth';

const Navbar = () => {
  const { colorMode, toggleColorMode } = useColorMode();
  const { logout } = useAuth();
  const navigate = useNavigate();
  const bg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <Box
      as="header"
      position="fixed"
      top={0}
      left={0}
      right={0}
      zIndex={10}
      borderBottomWidth="1px"
      borderBottomColor={borderColor}
      bg={bg}
      boxShadow="sm"
    >
      <Flex maxW="7xl" mx="auto" px={4} h={16} alignItems="center" justifyContent="space-between">
        <Flex alignItems="center">
          <Text as={RouterLink} to="/" fontWeight="bold" fontSize="xl" mr={8}>
            Kite Trader
          </Text>
          <Flex as="nav" display={{ base: 'none', md: 'flex' }} gap={4}>
            <Button as={RouterLink} to="/" variant="ghost">
              Dashboard
            </Button>
            <Button as={RouterLink} to="/orders" variant="ghost">
              Orders
            </Button>
            <Button as={RouterLink} to="/positions" variant="ghost">
              Positions
            </Button>
          </Flex>
        </Flex>

        <Flex alignItems="center" gap={4}>
          <Button onClick={toggleColorMode} variant="ghost" size="sm">
            {colorMode === 'light' ? <MoonIcon /> : <SunIcon />}
          </Button>
          <Button as={RouterLink} to="/profile" variant="ghost" size="sm">
            Profile
          </Button>
          <Button colorScheme="red" size="sm" onClick={handleLogout}>
            Logout
          </Button>
        </Flex>
      </Flex>
    </Box>
  );
};

export default Navbar;
