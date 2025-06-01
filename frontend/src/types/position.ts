export interface Position {
  // Core position data
  tradingsymbol: string;
  exchange: string;
  instrument_token: number;
  product: string;
  quantity: number;
  average_price: number;
  last_price: number;
  
  // P&L related
  pnl: number;
  day_pnl: number;
  day_change: number;
  day_change_percentage: number;
  m2m: number;
  
  // Buy/Sell details
  buy_price: number;
  buy_quantity: number;
  buy_value: number;
  sell_price: number;
  sell_quantity: number;
  sell_value: number;
  
  // Additional fields
  multiplier: number;
  realized: number;
  unrealized: number;  // Using American spelling consistently
  value: number;
  collateral_quantity: number;
  collateral_type: string;
  
  // Optional fields from API that might be present
  close_price?: number;
  day_buy_price?: number;
  day_buy_quantity?: number;
  day_buy_value?: number;
  day_sell_price?: number;
  day_sell_quantity?: number;
  day_sell_value?: number;
  overnight_quantity?: number;
}
