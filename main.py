import gc
import config
from machine import deepsleep, reset

try:
    from weather_display.utils import connect_wifi, disconnect_wifi

    connect_wifi(config.SSID, config.PASSWORD)
    gc.collect()

    from weather_display.client import fetch_weather

    weather = fetch_weather()
    gc.collect()

    disconnect_wifi()
    gc.collect()

    from weather_display.formatter import generate_data_frame

    data_frame = generate_data_frame(weather[0])
    gc.collect()

    from weather_display.epaper import EPaper

    epaper = EPaper()
    epaper.config()
    epaper.display_frame(data_frame)
    epaper.sleep()
    gc.collect()

    deepsleep(900000)  # Sleep for 15 mins
except MemoryError:
    reset()
