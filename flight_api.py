import json

def search_flights(parsed_data_json):
    try:
        data = json.loads(parsed_data_json)
    except:
        return []
    
    return [{
        "from": data.get("origin"),
        "to": data.get("destination"),
        "date": data.get("date"),
        "price": "499 PLN",
        "airline": "LOT"
    }]
