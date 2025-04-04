import os
import alpaca_trade_api as tradeapi
from typing import Dict, Any, Tuple
import httpx

class CryptoService:
    def __init__(self):
        self.api_key = os.getenv("ALPACA_API_KEY")
        self.api_secret = os.getenv("ALPACA_API_SECRET")
        self.alpaca = tradeapi.REST(self.api_key, self.api_secret, base_url='https://paper-api.alpaca.markets')
        
        # Crypto symbol mappings (symbol -> name)
        self.crypto_names = {
            "BTC": "Bitcoin",
            "ETH": "Ethereum",
            "SOL": "Solana",
            "ADA": "Cardano",
            "DOT": "Polkadot",
            "DOGE": "Dogecoin",
            "SHIB": "Shiba Inu",
            "AVAX": "Avalanche",
            "MATIC": "Polygon",
            "LTC": "Litecoin"
        }
        
    async def get_crypto_price(self, symbol: str) -> Tuple[Dict[str, Any], str]:
        """
        Get current price and data for a cryptocurrency.
        
        Args:
            symbol: Cryptocurrency symbol (e.g., "BTC", "ETH")
            
        Returns:
            Tuple of (crypto data dict, cryptocurrency name)
            
        Raises:
            Exception: If price retrieval fails
        """
        # Normalize symbol to uppercase
        symbol = symbol.upper()
        
        # Add USD suffix for Alpaca API
        alpaca_symbol = f"{symbol}USD"
        
        try:
            # Try to get data from Alpaca API
            crypto_data = self._get_from_alpaca(alpaca_symbol)
            
            # Get cryptocurrency name
            crypto_name = self.crypto_names.get(symbol, f"{symbol} Cryptocurrency")
            
            return crypto_data, crypto_name
            
        except Exception as e:
            print(f"Alpaca API error: {str(e)}")
            
            # Fallback to using CoinGecko API
            try:
                return await self._get_from_coingecko(symbol)
            except Exception as e2:
                print(f"CoinGecko API error: {str(e2)}")
                
                # If both APIs fail, return mock data for demo purposes
                return self._get_mock_data(symbol), self.crypto_names.get(symbol, f"{symbol} Cryptocurrency")
    
    def _get_from_alpaca(self, symbol: str) -> Dict[str, Any]:
        """
        Get cryptocurrency data from Alpaca API.
        
        Args:
            symbol: Cryptocurrency symbol with USD suffix
            
        Returns:
            Crypto data dictionary
            
        Raises:
            Exception: If API call fails
        """
        try:
            # Get last trade data
            trade = self.alpaca.get_latest_crypto_trade(symbol)
            
            # Get 24h bar data
            bars = self.alpaca.get_crypto_bars(symbol, "1Day").df
            
            if len(bars) == 0:
                raise Exception("No bar data available")
                
            # Calculate 24h change percentage
            open_price = bars.iloc[0]['open']
            close_price = bars.iloc[-1]['close']
            change_24h = ((close_price - open_price) / open_price) * 100
            
            # Market cap is not directly available from Alpaca
            # This is a placeholder calculation (not accurate)
            # In a real app, you would get this from another API
            if symbol.startswith("BTC"):
                market_cap = trade.price * 19_000_000  # ~19M BTC in circulation
            elif symbol.startswith("ETH"):
                market_cap = trade.price * 120_000_000  # ~120M ETH in circulation
            else:
                market_cap = trade.price * 1_000_000_000  # Placeholder
            
            # 24h volume from bar data
            volume_24h = bars['volume'].sum()
            
            return {
                "price": trade.price,
                "change_24h": change_24h,
                "market_cap": market_cap,
                "volume_24h": volume_24h
            }
            
        except Exception as e:
            raise Exception(f"Error retrieving data from Alpaca: {str(e)}")
    
    async def _get_from_coingecko(self, symbol: str) -> Tuple[Dict[str, Any], str]:
        """
        Get cryptocurrency data from CoinGecko API.
        
        Args:
            symbol: Cryptocurrency symbol
            
        Returns:
            Tuple of (crypto data dict, cryptocurrency name)
            
        Raises:
            Exception: If API call fails
        """
        # CoinGecko requires IDs instead of symbols
        symbol_to_id = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "SOL": "solana",
            "ADA": "cardano",
            "DOT": "polkadot",
            "DOGE": "dogecoin",
            "SHIB": "shiba-inu",
            "AVAX": "avalanche-2",
            "MATIC": "matic-network",
            "LTC": "litecoin"
        }
        
        coin_id = symbol_to_id.get(symbol)
        if not coin_id:
            raise Exception(f"Unknown cryptocurrency symbol: {symbol}")
        
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                
                if response.status_code != 200:
                    raise Exception(f"CoinGecko API error: {response.text}")
                    
                data = response.json()
                
                crypto_data = {
                    "price": data["market_data"]["current_price"]["usd"],
                    "change_24h": data["market_data"]["price_change_percentage_24h"],
                    "market_cap": data["market_data"]["market_cap"]["usd"],
                    "volume_24h": data["market_data"]["total_volume"]["usd"]
                }
                
                crypto_name = data["name"]
                
                return crypto_data, crypto_name
                
        except Exception as e:
            raise Exception(f"Error retrieving data from CoinGecko: {str(e)}")
    
    def _get_mock_data(self, symbol: str) -> Dict[str, Any]:
        """
        Get mock cryptocurrency data for demo purposes.
        
        Args:
            symbol: Cryptocurrency symbol
            
        Returns:
            Mock crypto data dictionary
        """
        mock_data = {
            "BTC": {
                "price": 51432.78,
                "change_24h": 2.3,
                "market_cap": 986.7 * 1_000_000_000,
                "volume_24h": 32.4 * 1_000_000_000
            },
            "ETH": {
                "price": 2815.42,
                "change_24h": 1.8,
                "market_cap": 338.5 * 1_000_000_000,
                "volume_24h": 18.2 * 1_000_000_000
            },
            "SOL": {
                "price": 149.87,
                "change_24h": 4.5,
                "market_cap": 63.7 * 1_000_000_000,
                "volume_24h": 5.8 * 1_000_000_000
            },
            "DOGE": {
                "price": 0.12,
                "change_24h": -1.2,
                "market_cap": 16.8 * 1_000_000_000,
                "volume_24h": 1.2 * 1_000_000_000
            }
        }
        
        # Return data for the symbol, or BTC data as default
        return mock_data.get(symbol, mock_data["BTC"]) 