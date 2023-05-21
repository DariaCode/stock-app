/* eslint-disable camelcase */
export interface Stock {
  date: string;
  value: number;
  price: number;
}

export interface PerformanceData {
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  annualized_return: number;
  annualized_volatility: number;
  cumulative_return: number;
}
