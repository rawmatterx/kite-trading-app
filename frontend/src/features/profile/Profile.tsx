import { Box, Heading, VStack, Text, Stat, StatLabel, StatNumber, StatHelpText, useColorModeValue, Button, useToast, SimpleGrid } from '@chakra-ui/react';
import { useQuery } from '@tanstack/react-query';
import { useAuth } from '../../hooks/useAuth';
import api from '../../services/api';

const Profile = () => {
  const { logout } = useAuth();
  const toast = useToast();
  
  const { data: profile, isLoading } = useQuery({ 
    queryKey: ['profile'], 
    queryFn: async () => {
      const response = await api.get('/profile');
      return response.data;
    }
  });

  const handleLogout = () => {
    logout();
    toast({
      title: 'Logged out successfully',
      status: 'info',
      duration: 3000,
      isClosable: true,
    });  
  };

  const cardBg = useColorModeValue('white', 'gray.700');

  if (isLoading) {
    return <Box>Loading profile...</Box>;
  }

  return (
    <Box p={4} maxW="4xl" mx="auto">
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={8}>
        <Heading as="h1" size="xl">
          Profile
        </Heading>
        <Button colorScheme="red" variant="outline" onClick={handleLogout}>
          Logout
        </Button>
      </Box>

      <Box
        borderWidth="1px"
        borderRadius="lg"
        p={6}
        bg={cardBg}
        boxShadow="sm"
        mb={8}
      >
        <VStack spacing={6} align="stretch">
          <Box>
            <Text fontSize="sm" color="gray.500" mb={1}>
              Name
            </Text>
            <Text fontSize="lg" fontWeight="medium">
              {profile?.user?.name || 'N/A'}
            </Text>
          </Box>

          <Box>
            <Text fontSize="sm" color="gray.500" mb={1}>
              Email
            </Text>
            <Text fontSize="lg" fontWeight="medium">
              {profile?.user?.email || 'N/A'}
            </Text>
          </Box>

          <Box>
            <Text fontSize="sm" color="gray.500" mb={1}>
              User ID
            </Text>
            <Text fontFamily="mono" fontSize="sm">
              {profile?.user?.user_id || 'N/A'}
            </Text>
          </Box>
        </VStack>
      </Box>

      <Heading size="lg" mb={4}>
        Account Details
      </Heading>

      <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6} mb={8}>
        <Stat p={4} borderWidth="1px" borderRadius="lg" bg={cardBg} boxShadow="sm">
          <StatLabel>Available Balance</StatLabel>
          <StatNumber>₹{profile?.balance?.available_balance?.toFixed(2) || '0.00'}</StatNumber>
          <StatHelpText>Available for trading</StatHelpText>
        </Stat>

        <Stat p={4} borderWidth="1px" borderRadius="lg" bg={cardBg} boxShadow="sm">
          <StatLabel>Used Margin</StatLabel>
          <StatNumber>₹{profile?.balance?.used_margin?.toFixed(2) || '0.00'}</StatNumber>
          <StatHelpText>Margin used in positions</StatHelpText>
        </Stat>

        <Stat p={4} borderWidth="1px" borderRadius="lg" bg={cardBg} boxShadow="sm">
          <StatLabel>Net Value</StatLabel>
          <StatNumber>₹{profile?.balance?.net?.toFixed(2) || '0.00'}</StatNumber>
          <StatHelpText>Total portfolio value</StatHelpText>
        </Stat>
      </SimpleGrid>

      <Box
        borderWidth="1px"
        borderRadius="lg"
        p={6}
        bg={cardBg}
        boxShadow="sm"
      >
        <Heading size="md" mb={4}>
          Trading Statistics
        </Heading>
        <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
          <Stat p={4} borderWidth="1px" borderRadius="md">
            <StatLabel>Total Trades</StatLabel>
            <StatNumber>{profile?.statistics?.total_trades || 0}</StatNumber>
            <StatHelpText>All time</StatHelpText>
          </Stat>
          
          <Stat p={4} borderWidth="1px" borderRadius="md">
            <StatLabel>Win Rate</StatLabel>
            <StatNumber>{(profile?.statistics?.win_rate || 0).toFixed(1)}%</StatNumber>
            <StatHelpText>Successful trades</StatHelpText>
          </Stat>
          
          <Stat p={4} borderWidth="1px" borderRadius="md">
            <StatLabel>Average Profit</StatLabel>
            <StatNumber>₹{(profile?.statistics?.avg_profit || 0).toFixed(2)}</StatNumber>
            <StatHelpText>Per winning trade</StatHelpText>
          </Stat>
          
          <Stat p={4} borderWidth="1px" borderRadius="md">
            <StatLabel>Average Loss</StatLabel>
            <StatNumber>₹{Math.abs(profile?.statistics?.avg_loss || 0).toFixed(2)}</StatNumber>
            <StatHelpText>Per losing trade</StatHelpText>
          </Stat>
        </SimpleGrid>
      </Box>
    </Box>
  );
};

export default Profile;
