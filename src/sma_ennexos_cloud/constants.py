CLIENT_ID = "SPpbeOS"
AUTH_BASE = "https://login.sma.energy/auth/realms/SMA"
TOKEN_URL = f"{AUTH_BASE}/protocol/openid-connect/token"
AUTH_URL = f"{AUTH_BASE}/protocol/openid-connect/auth"
REDIRECT_URI = "https://ennexos.sunnyportal.com/dashboard/initialize"
API_BASE = "https://uiapi.sunnyportal.com/api/v1"

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/150.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "sec-ch-ua": '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
}

AUTH_PAGE_HEADERS = {
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    ),
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Upgrade-Insecure-Requests": "1",
}

LOGIN_POST_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "null",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Upgrade-Insecure-Requests": "1",
}

TOKEN_POST_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://ennexos.sunnyportal.com",
    "Referer": "https://ennexos.sunnyportal.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
}

API_REQUEST_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://ennexos.sunnyportal.com",
    "Referer": "https://ennexos.sunnyportal.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
}

STATUS_PAGE_SUMMARY_URL = "https://sunnyportal.statuspage.io/api/v2/summary.json"
ENNEXOS_GROUP_ID = "0t5wbfgnxjs4"
ENNEXOS_LIVE_DATA_COMPONENT_ID = "2vkfhwrgmzqf"

WEATHER_DESCRIPTIONS: dict[int, str] = {
    0: "Cloudless",
    1: "Slightly cloudy",
    2: "Cloudy",
    3: "Heavy cloud or overcast",
    10: "Fog",
    11: "Fog with frost",
    16: "Sandstorm",
    20: "Drizzle",
    21: "Drizzle, freezing",
    30: "Light rain",
    31: "Moderate rain",
    32: "Heavy rain",
    40: "Light rain, freezing",
    41: "Moderate or heavy rain, freezing",
    50: "Light snowfall",
    51: "Moderate snowfall",
    52: "Heavy snowfall",
    53: "Sleet",
    60: "Light rain shower",
    61: "Moderate or heavy rain shower",
    62: "Very heavy rain shower",
    70: "Light snow shower",
    71: "Moderate or heavy snow shower",
    80: "Light or moderate thunderstorm",
    81: "Heavy thunderstorm (or thunderstorm with sleet/hail)",
    90: "Cloudless",
    91: "Cloudless",
}

WEATHER_ICON_FILES: dict[int, str] = {
    0: "800D.png",
    1: "801D.png",
    2: "803D.png",
    3: "804.png",
    10: "701.png",
    11: "900.png",
    16: "701.png",
    20: "503.png",
    21: "611.png",
    30: "500.png",
    31: "501.png",
    32: "502.png",
    40: "611.png",
    41: "621.png",
    50: "600.png",
    51: "601.png",
    52: "602.png",
    53: "511.png",
    60: "520.png",
    61: "521.png",
    62: "522.png",
    70: "600.png",
    71: "602.png",
    80: "211.png",
    81: "202.png",
    90: "800D.png",
    91: "800D.png",
}

WEATHER_CONDITION_MAP: dict[int, str] = {
    0: "sunny",
    1: "partlycloudy",
    2: "cloudy",
    3: "cloudy",
    10: "fog",
    11: "fog",
    16: "exceptional",
    20: "rainy",
    21: "rainy",
    30: "rainy",
    31: "rainy",
    32: "pouring",
    40: "snowy-rainy",
    41: "snowy-rainy",
    50: "snowy",
    51: "snowy",
    52: "snowy",
    53: "snowy-rainy",
    60: "rainy",
    61: "rainy",
    62: "pouring",
    70: "snowy",
    71: "snowy",
    80: "lightning",
    81: "lightning-rainy",
    90: "sunny",
    91: "sunny",
}


def normalize_weather_icon_id(icon_id: int) -> int:
    """Normalize weather icon ID (e.g. 100+ mapped modulo 100 per SMA ennexOS web app)."""
    return icon_id % 100 if icon_id >= 100 else icon_id

