import requests

def lookup(symbol):
    

    # Reject symbol if it starts with caret
    if symbol.startswith("^"):
        return None

    # Reject symbol if it contains comma
    if "," in symbol:
        return None

    api_key = "a74c1d6a9bfc48a096826ab16608dd72"
    url = f"https://api.twelvedata.com/quote?symbol={symbol}&apikey={api_key}"

    try:
        response = requests.get(url).json()
        
        if "code" in response:
            # Handling error response
            return None

        # Return stock's name, price, and symbol
        return {
            "price": response.get("close"),
            "company": response.get("name"),
            "symbol": symbol.upper()
        }

    except requests.RequestException as e:
        print(f"Request error fetching data: {e}")
        return None
    except KeyError as e:
        print(f"KeyError fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
