from pycoingecko import CoinGeckoAPI

# Initialize API client 
cg = CoinGeckoAPI()

def get_bitcoin_summary() -> str:
    
    coin = cg.get_coin_by_id('bitcoin')

    # Extract key figures
    name = coin['name']
    symbol = coin['symbol'].upper()
    price = coin['market_data']['current_price']['usd']
    market_cap = coin['market_data']['market_cap']['usd']
    change_24h = coin['market_data']['price_change_percentage_24h']
    supply = coin['market_data']['circulating_supply']

    # Format clean summary
    summary = (
        f"📊 {name} ({symbol})\n"
        f"💰 Price: ${price:,.2f}\n"
        f"🏦 Market Cap: ${market_cap:,.0f}\n"
        f"📈 24h Change: {change_24h:.2f}%\n"
        f"🔄 Circulating Supply: {supply:,.0f} {symbol}"
    )
    return summary

# Example usage
if __name__ == "__main__":
    print(get_bitcoin_summary())
