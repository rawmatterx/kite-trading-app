import { extendTheme } from '@chakra-ui/react';

const theme = extendTheme({
  colors: {
    brand: {
      50: '#e6f7ff',
      100: '#b3e0ff',
      200: '#80c9ff',
      300: '#4db3ff',
      400: '#1a9cff',
      500: '#0080ff',
      600: '#0066cc',
      700: '#004d99',
      800: '#003366',
      900: '#001a33',
    },
  },
  config: {
    initialColorMode: 'light',
    useSystemColorMode: false,
  },
});

export default theme;
