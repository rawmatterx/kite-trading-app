import api from './api';
import type { AxiosResponse } from 'axios';

interface MarginsResponse {
  equity?: {
    enabled: boolean;
    net: number;
    available: {
      adhoc_margin: number;
      cash: number;
      opening_balance: number;
      live_balance: number;
      collateral: number;
      intraday_payin: number;
    };
    utilised: {
      debits: number;
      exposure: number;
      m2m_realised: number;
      m2m_unrealised: number;
      option_premium: number;
      payout: number;
      span: number;
      holding_sales: number;
      turnover: number;
    };
  };
  commodity?: any; // Define this interface if you need to use commodity margins
}

interface PositionsResponse {
  net: Array<{
    average_price: number;
    buy_m2m: number;
    buy_price: number;
    buy_quantity: number;
    buy_value: number;
    close_price: number;
    day_buy_price: number;
    day_buy_quantity: number;
    day_buy_value: number;
    day_sell_price: number;
    day_sell_quantity: number;
    day_sell_value: number;
    exchange: string;
    instrument_token: number;
    last_price: number;
    m2m: number;
    multiplier: number;
    overnight_quantity: number;
    pnl: number;
    product: string;
    quantity: number;
    sell_m2m: number;
    sell_price: number;
    sell_quantity: number;
    sell_value: number;
    tradingsymbol: string;
    unrealised: number;
    value: number;
  }>;
  day: Array<{
    average_price: number;
    buy_m2m: number;
    buy_price: number;
    buy_quantity: number;
    buy_value: number;
    close_price: number;
    day_buy_price: number;
    day_buy_quantity: number;
    day_buy_value: number;
    day_sell_price: number;
    day_sell_quantity: number;
    day_sell_value: number;
    exchange: string;
    instrument_token: number;
    last_price: number;
    m2m: number;
    multiplier: number;
    overnight_quantity: number;
    pnl: number;
    product: string;
    quantity: number;
    sell_m2m: number;
    sell_price: number;
    sell_quantity: number;
    sell_value: number;
    tradingsymbol: string;
    unrealised: number;
    value: number;
  }>; // Define this interface if you need to use day positions
}

export const getMargins = async (): Promise<MarginsResponse> => {
  try {
    const response: AxiosResponse<MarginsResponse> = await api.get('/api/v1/margins');
    return response.data;
  } catch (error) {
    console.error('Error fetching margins:', error);
    throw error;
  }
};

export const getPositions = async (): Promise<PositionsResponse> => {
  try {
    const response: AxiosResponse<PositionsResponse> = await api.get('/api/v1/positions');
    return response.data;
  } catch (error) {
    console.error('Error fetching positions:', error);
    throw error;
  }
};

interface Holding {
  average_price: number;
  collateral_quantity: number;
  collateral_type: string;
  day_change: number;
  day_change_percentage: number;
  exchange: string;
  instrument_token: number;
  isin: string;
  last_price: number;
  pnl: number;
  price: number;
  product: string;
  quantity: number;
  t1_quantity: number;
  tradingsymbol: string;
  used_quantity: number;
}

export const getHoldings = async (): Promise<Holding[]> => {
  try {
    const response = await api.get('/api/v1/holdings');
    return response.data;
  } catch (error) {
    console.error('Error fetching holdings:', error);
    throw error;
  }
};
