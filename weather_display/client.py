def fetch_weather():
    import gc
    import requests

    print("Fetching Weather Data...")
    response = requests.get("https://wttr.in/?format=j1")
    data = response.json()["current_condition"]
    response.close()
    gc.collect()
    return data
