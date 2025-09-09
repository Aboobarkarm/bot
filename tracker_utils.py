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
    table = "📊 <b>Crypto Price Tracker</b>\n\n"

    data = cg.get_price(ids=",".join(targets.keys()), vs_currencies="usd")

    for coin, target in targets.items():
        price = data[coin]["usd"]
        status = "✅ <b>Met</b>" if price >= target else "❌ <i>Not yet</i>"

        symbol = coin_info[coin]["symbol"]
        logo = coin_info[coin]["logo"]
        name = coin.capitalize()

        # add line spacing for readability
        table += (
            f"{logo} <b>{name}</b> ({symbol})\n"
            f"🎯 Target: <code>${format_price(target)}</code>\n"
            f"💰 Current: <code>${format_price(price)}</code>\n"
            f"📌 Status: {status}\n\n"
        )

    return table


# Example usage
if __name__ == "__main__":
    print(track_coins_summary())
