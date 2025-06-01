import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { ChakraProvider, extendTheme } from '@chakra-ui/react'
import './index.css'
import App from './App.tsx'

// Extend the theme to include custom colors, fonts, etc.
const theme = extendTheme({
  // Add your custom theme here
  config: {
    initialColorMode: 'light',
    useSystemColorMode: false,
  },
  // Add any other theme customizations here
});

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ChakraProvider theme={theme}>
      <App />
    </ChakraProvider>
  </StrictMode>,
)
