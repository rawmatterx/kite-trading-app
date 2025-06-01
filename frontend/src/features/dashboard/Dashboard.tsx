import React from 'react';
import { Box, Button, Flex, Heading, SimpleGrid, Text, useToast } from '@chakra-ui/react';
import { Card, CardBody, CardHeader } from '@chakra-ui/card';
import { Table, Thead, Tbody, Tr, Th, Td } from '@chakra-ui/table';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { getMargins, getPositions } from '../../services/kiteService';

// Import Position type from the shared types
import type { Position } from '../../types/position';

const Dashboard = () => {
  const toast = useToast();

  // Fetch margins data
  const {
    data: marginsData,
    isLoading: isLoadingMargins,
    error: marginsError,
  } = useQuery({
    queryKey: ['margins'],
    queryFn: getMargins,
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  // Show error toast for margins fetch
  React.useEffect(() => {
    if (marginsError) {
      toast({
        title: 'Error fetching margins',
        description: marginsError.message || 'Failed to fetch margin data',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  }, [marginsError, toast]);

  // Fetch positions data
  const {
    data: positionsData,
    isLoading: isLoadingPositions,
    error: positionsError,
  } = useQuery({
    queryKey: ['positions'],
    queryFn: async (): Promise<Position[]> => {
      const data = await getPositions();
      // Map the API response to our Position type
      return (data.net || []).map(pos => ({
        tradingsymbol: pos.tradingsymbol,
        exchange: pos.exchange,
        instrument_token: pos.instrument_token,
        product: pos.product,
        quantity: pos.quantity,
        average_price: pos.average_price,
        last_price: pos.last_price,
        pnl: pos.pnl,
        day_pnl: 0, // Will be calculated or updated from API if available
        day_change: 0, // Will be calculated or updated from API if available
        day_change_percentage: 0, // Will be calculated or updated from API if available
        m2m: 0, // Will be updated from API if available
        buy_price: 0, // Will be updated from API if available
        buy_quantity: 0, // Will be updated from API if available
        buy_value: 0, // Will be updated from API if available
        sell_price: 0, // Will be updated from API if available
        sell_quantity: 0, // Will be updated from API if available
        sell_value: 0, // Will be updated from API if available
        multiplier: 1, // Default value, update if available
        realized: 0, // Will be updated from API if available
        unrealized: pos.unrealised || 0, // Using API's unrealised value
        value: pos.value || 0,
        collateral_quantity: 0, // Default value, update if available
        collateral_type: '' // Default value, update if available
      }));
    },
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  // Show error toast for positions fetch
  React.useEffect(() => {
    if (positionsError) {
      toast({
        title: 'Error fetching positions',
        description: positionsError.message || 'Failed to fetch positions data',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  }, [positionsError, toast]);

  const isLoading = isLoadingMargins || isLoadingPositions;
  const error = marginsError || positionsError;

  if (isLoading) {
    return (
      <Box p={4}>
        <Text>Loading dashboard data...</Text>
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={4}>
        <Text color="red.500">Error loading dashboard data. Please try again later.</Text>
      </Box>
    );
  }

  return (
    <Box p={4}>
      <Flex justify="space-between" mb={6}>
        <Heading size="lg">Dashboard</Heading>
        <Button as={Link} to="/orders/new" colorScheme="blue">
          New Order
        </Button>
      </Flex>

      <SimpleGrid columns={{ base: 1, md: 3 }} spacing={4} mb={6}>
        <Card>
          <CardHeader>
            <Text fontSize="sm" color="gray.500">Available Margin</Text>
            <Heading size="lg">
              ₹{(marginsData?.equity?.available?.cash ?? 0).toLocaleString('en-IN')}
            </Heading>
          </CardHeader>
          <CardBody pt={0}>
            <Text fontSize="sm" color="gray.500">
              Net: ₹{(marginsData?.equity?.net ?? 0).toLocaleString('en-IN')}
            </Text>
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <Text fontSize="sm" color="gray.500">Used Margin</Text>
            <Heading size="lg">
              ₹{(marginsData?.equity?.utilised?.span ?? 0).toLocaleString('en-IN')}
            </Heading>
          </CardHeader>
          <CardBody pt={0}>
            <Text fontSize="sm" color="gray.500">
              Exposure: ₹{(marginsData?.equity?.utilised?.exposure ?? 0).toLocaleString('en-IN')}
            </Text>
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <Text fontSize="sm" color="gray.500">Unrealized P&L</Text>
            <Heading 
              size="lg" 
              color={(marginsData?.equity?.utilised?.m2m_unrealised ?? 0) >= 0 ? 'green.500' : 'red.500'}
            >
              {(marginsData?.equity?.utilised?.m2m_unrealised ?? 0) >= 0 ? '+' : ''}
              ₹{Math.abs(marginsData?.equity?.utilised?.m2m_unrealised ?? 0).toLocaleString('en-IN')}
            </Heading>
          </CardHeader>
          <CardBody pt={0}>
            <Text fontSize="sm" color="gray.500">
              Realized: ₹{(marginsData?.equity?.utilised?.m2m_realised ?? 0).toLocaleString('en-IN')}
            </Text>
          </CardBody>
        </Card>
      </SimpleGrid>

      <Card mb={6}>
        <CardHeader>
          <Heading size="md">Positions</Heading>
        </CardHeader>
        <CardBody>
          {positionsData && positionsData.length > 0 ? (
            <Table variant="simple" size="sm">
              <Thead>
                <Tr>
                  <Th>Symbol</Th>
                  <Th isNumeric>Qty</Th>
                  <Th isNumeric>Avg. Price</Th>
                  <Th isNumeric>LTP</Th>
                  <Th isNumeric>P&L</Th>
                  <Th isNumeric>Value</Th>
                </Tr>
              </Thead>
              <Tbody>
                {positionsData
                  .filter((p: Position) => p.quantity !== 0)
                  .map((position) => (
                    <Tr key={`${position.tradingsymbol}-${position.exchange}`}>
                      <Td>
                        <Text fontWeight="bold">{position.tradingsymbol}</Text>
                        <Text fontSize="xs" color="gray.500">
                          {position.exchange} • {position.product}
                        </Text>
                      </Td>
                      <Td isNumeric>{position.quantity}</Td>
                      <Td isNumeric>₹{position.average_price?.toFixed(2)}</Td>
                      <Td isNumeric>₹{position.last_price?.toFixed(2)}</Td>
                      <Td 
                        isNumeric 
                        color={position.unrealized >= 0 ? 'green.500' : 'red.500'}
                      >
                        {position.unrealized >= 0 ? '+' : ''}
                        ₹{Math.abs(position.unrealized || 0).toFixed(2)}
                      </Td>
                      <Td isNumeric>
                        ₹{Math.abs(position.value || 0).toFixed(2)}
                      </Td>
                    </Tr>
                  ))}
              </Tbody>
            </Table>
          ) : (
            <Text>No open positions</Text>
          )}
        </CardBody>
      </Card>

      <Box mb={8}>
        <Flex justify="space-between" align="center" mb={4}>
          <Heading size="md">Recent Orders</Heading>
          <Button as={Link} to="/orders" size="sm" variant="outline">
            View All
          </Button>
        </Flex>
        <Text>No recent orders to display</Text>
      </Box>
    </Box>
  );
};

export default Dashboard;
