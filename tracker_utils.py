from pycoingecko import CoinGeckoAPI

# Initialize API client 
cg = CoinGeckoAPI()

# Example targets
targets = {
    "bitcoin": 60000,
    "ethereum": 4000,
    "shiba-inu": 0.00002,
    "ripple": 3.03, 
}


coin_info = {
    "bitcoin":  {"symbol": "BTC", "logo": "🟠"},
    "ethereum": {"symbol": "ETH", "logo": "💎"},
    "shiba-inu": {"symbol": "SHIB", "logo": "🐕"},
    "ripple":   {"symbol": "XRP", "logo": "💧"},
}

def format_price(value: float) -> str:
    if value < 1:
        return f"{value:.8f}"  
    else:
        return f"{value:,.2f}"  

def track_coins_summary() -> str:
    table = "📊 Crypto Price Tracker\n\n"
    
    for coin, target in targets.items():
        data = cg.get_price(ids=coin, vs_currencies="usd")
        price = data[coin]["usd"]
        status = "✅ Met" if price >= target else "❌ Not yet"

        symbol = coin_info[coin]["symbol"]
        logo = coin_info[coin]["logo"]
        name = coin.capitalize()

        table += (
            f"{logo} {name:9} ({symbol}) | "
            f"Target: ${format_price(target)} | "
            f"Current: ${format_price(price)} | "
            f"{status}\n"
        )

    return table

# Example usage
if __name__ == "__main__":
    print(track_coins_summary())
