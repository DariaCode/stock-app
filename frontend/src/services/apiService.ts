import axios from 'axios'

const API_BASE_URL = 'https://stock-market-21052023.ew.r.appspot.com/api' //  'http://127.0.0.1:5000/api'
const STOCKS_API_URL = `${API_BASE_URL}/stocks`
const PERFORMANCES_API_URL = `${API_BASE_URL}/performances`

export async function getStocksData () {
  const response = await axios.get(STOCKS_API_URL)
  return response.data
}

export async function getPerformancesData () {
  const response = await axios.get(PERFORMANCES_API_URL)
  return response.data
}
