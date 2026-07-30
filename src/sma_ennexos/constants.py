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
