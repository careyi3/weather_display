def __generate_from_string(input):
    from weather_display.press_start_2p import (
        FONT,
    )  # Change this if you want a different font

    buffer = []
    for y in range(0, 264):
        for x in range(0, 11):
            char = input[((y // 16) * 11) + x]
            char_bytes = FONT[ord(char)]
            segment = char_bytes[y % 16]
            buffer += segment
    return buffer


def generate_data_frame(weather_data):
    import gc
    from weather_display.weather_codes import CONDITIONS

    con = CONDITIONS[weather_data["weatherCode"]]
    gc.collect()

    temp = weather_data["temp_C"]
    feels_like = weather_data["FeelsLikeC"]
    wind_dir = weather_data["winddir16Point"]
    wind_speed = weather_data["windspeedKmph"]
    visibility = weather_data["visibility"]
    percipitation = weather_data["precipMM"]
    time = weather_data["observation_time"]
    gc.collect()

    lines = [
        f"           " f"           " f"           " f"           ",
        f" {con}",
        f"           ",
        f" {temp}({feels_like})'C",
        f" {wind_dir} {wind_speed}kmh",
        f" {visibility}km",
        f" {percipitation}mm",
        f"           ",
        f" @{time}",
        f"           ",
        f"           ",
        f"           " f"           " f"           " f"           ",
    ]

    padded_lines = []
    for line in lines:
        if len(line) == 11:
            padded_lines.append(line)
        else:
            padded_lines.append("{:<11}".format(line))

    input = "".join(padded_lines)
    gc.collect()

    return __generate_from_string(input)
