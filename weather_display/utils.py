def connect_wifi(ssid, password):
    import network

    print(f"Attempting to connect to: {ssid}")

    wlan = network.WLAN(network.WLAN.IF_STA)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass

    print(f"Connected to: {ssid}")
    print(f"IP: {wlan.ipconfig('addr4')}")


def disconnect_wifi():
    import network

    wlan = network.WLAN(network.WLAN.IF_STA)
    wlan.active(False)
