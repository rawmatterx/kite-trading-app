import { Box, Heading, Table, Thead, Tbody, Tr, Th, Td, Badge, Text, useColorModeValue } from '@chakra-ui/react';
import { useQuery } from '@tanstack/react-query';
import api from '../../services/api';
import type { Position } from '../../types/position';

const Positions = () => {
  const { data: positions, isLoading, error } = useQuery<Position[], Error>({
    queryKey: ['positions'],
    queryFn: async () => {
      const response = await api.get<Position[]>('/positions');
      return response.data;
    }
  });

  const bgColor = useColorModeValue('white', 'gray.700');

  const renderPnL = (value: number | undefined) => {
    if (value === undefined) return <Text>-</Text>;
    const isPositive = value >= 0;
    return (
      <Text color={isPositive ? 'green.500' : 'red.500'}>
        {isPositive ? '+' : ''}{value.toFixed(2)}
      </Text>
    );
  };

  if (isLoading) {
    return <Box p={4}>Loading positions...</Box>;
  }

  if (error) {
    return <Box p={4}>Error loading positions: {error.message}</Box>;
  }

  if (!positions?.length) {
    return (
      <Box p={4}>
        <Heading as="h1" size="xl" mb={6}>
          Positions
        </Heading>
        <Box p={6} textAlign="center" borderWidth="1px" borderRadius="lg" bg={bgColor} boxShadow="sm">
          <Text>No open positions</Text>
        </Box>
      </Box>
    );
  }

  return (
    <Box p={4}>
      <Heading as="h1" size="xl" mb={6}>
        Positions
      </Heading>
      <Box borderWidth="1px" borderRadius="lg" overflow="hidden" bg={bgColor} boxShadow="sm">
        <Table variant="simple">
          <Thead>
            <Tr>
              <Th>Symbol</Th>
              <Th>Quantity</Th>
              <Th>Avg. Price</Th>
              <Th>LTP</Th>
              <Th>P&L</Th>
              <Th>Day P&L</Th>
              <Th>Change</Th>
            </Tr>
          </Thead>
          <Tbody>
            {positions.map((position) => {
              const change = position.average_price ? 
                ((position.last_price - position.average_price) / position.average_price) * 100 : 0;
              const isPositive = change >= 0;
              
              return (
                <Tr key={`${position.tradingsymbol}-${position.product}`} _hover={{ bg: 'gray.50' }}>
                  <Td>
                    <Box>
                      <Text fontWeight="medium">{position.tradingsymbol}</Text>
                      <Text fontSize="sm" color="gray.500">{position.exchange}</Text>
                    </Box>
                  </Td>
                  <Td>
                    <Badge colorScheme={position.quantity > 0 ? 'green' : 'red'}>
                      {position.quantity > 0 ? 'LONG' : 'SHORT'} {Math.abs(position.quantity)}
                    </Badge>
                  </Td>
                  <Td>₹{position.average_price?.toFixed(2) || '-'}</Td>
                  <Td>₹{position.last_price?.toFixed(2) || '-'}</Td>
                  <Td>{renderPnL(position.pnl)}</Td>
                  <Td>{renderPnL(position.day_pnl)}</Td>
                  <Td color={isPositive ? 'green.500' : 'red.500'}>
                    {isPositive ? '↑' : '↓'} {Math.abs(change).toFixed(2)}%
                  </Td>
                </Tr>
              );
            })}
          </Tbody>
        </Table>
      </Box>
    </Box>
  );
};

export default Positions;
