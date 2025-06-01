export interface Position {
  tradingsymbol: string;
  exchange: string;
  instrument_token: number;
  product: string;
  quantity: number;
  average_price: number;
  last_price: number;
  pnl: number;
  day_pnl: number;
  day_change: number;
  day_change_percentage: number;
  m2m: number;
  buy_price: number;
  buy_quantity: number;
  buy_value: number;
  sell_price: number;
  sell_quantity: number;
  sell_value: number;
  multiplier: number;
  realized: number;
  unrealized: number;
  value: number;
  collateral_quantity: number;
  collateral_type: string;
}
