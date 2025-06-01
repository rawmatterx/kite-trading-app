import { Box, Heading, Table, Thead, Tbody, Tr, Th, Td, Badge, Text, useColorModeValue } from '@chakra-ui/react';
import { useQuery } from '@tanstack/react-query';
import api from '../../services/api';

interface Order {
  order_id: string;
  tradingsymbol: string;
  transaction_type: 'BUY' | 'SELL';
  quantity: number;
  average_price: number | null;
  status: string;
  order_timestamp: string;
  // Add other order properties as needed
}

const statusColorMap: { [key: string]: string } = {
  'COMPLETE': 'green',
  'OPEN': 'blue',
  'CANCELLED': 'red',
  'REJECTED': 'red',
  'TRIGGER_PENDING': 'orange',
  'VALIDATION_PENDING': 'yellow',
};

const Orders = () => {
  const { data: orders = [], isLoading, error } = useQuery<Order[]>({
    queryKey: ['orders'],
    queryFn: async () => {
      try {
        const response = await api.get<{ data: Order[] }>('/orders');
        return response.data?.data || [];
      } catch (error) {
        console.error('Error fetching orders:', error);
        return [];
      }
    }
  });

  const bgColor = useColorModeValue('white', 'gray.700');

  if (isLoading) {
    return <Box>Loading orders...</Box>;
  }

  if (error) {
    return <Box>Error loading orders</Box>;
  }

  return (
    <Box p={4}>
      <Heading as="h1" size="xl" mb={6}>
        Orders
      </Heading>

      <Box borderWidth="1px" borderRadius="lg" overflow="hidden" bg={bgColor} boxShadow="sm">
        {orders.length > 0 ? (
          <Table variant="simple">
            <Thead>
              <Tr>
                <Th>Order ID</Th>
                <Th>Trading Symbol</Th>
                <Th>Type</Th>
                <Th>Quantity</Th>
                <Th>Price</Th>
                <Th>Status</Th>
                <Th>Time</Th>
              </Tr>
            </Thead>
            <Tbody>
              {orders.map((order) => (
                <Tr key={order.order_id} _hover={{ bg: 'gray.50' }}>
                  <Td fontSize="sm" fontFamily="mono">{order.order_id}</Td>
                  <Td fontWeight="medium">{order.tradingsymbol}</Td>
                  <Td>
                    <Badge 
                      colorScheme={
                        order.transaction_type === 'BUY' ? 'green' : 'red'
                      }
                    >
                      {order.transaction_type}
                    </Badge>
                  </Td>
                  <Td>{order.quantity}</Td>
                  <Td>₹{order.average_price || 'Market'}</Td>
                  <Td>
                    <Badge colorScheme={statusColorMap[order.status] || 'gray'}>
                      {order.status}
                    </Badge>
                  </Td>
                  <Td>{new Date(order.order_timestamp).toLocaleString()}</Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        ) : (
          <Box p={6} textAlign="center">
            <Text>No orders found</Text>
          </Box>
        )}
      </Box>
    </Box>
  );
};

export default Orders;
