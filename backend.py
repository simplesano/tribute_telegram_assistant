import httpx, asyncio, hmac, hashlib
from env import BACKEND_URL, BACKEND_KEY  # type: ignore
# from typing import Optional

if not BACKEND_URL or not BACKEND_KEY:
    raise RuntimeError("SERVER_URL and SERVER_KEY must be set")

"""
Activate purchase at the backend.

Attempts:
    1st → immediately
    2nd → after 10s if not 202
    4th → after 60s if still not 202, then logs error
"""

DELAYS = [0, 10, 60]  # 3 attempts, delayed in seconds

def log(text):
    print(text, flush=True)


# Shared HTTP client (important for Railway)
_http_client: httpx.AsyncClient | None = None

def get_http_client() -> httpx.AsyncClient:
    global _http_client

    if _http_client is None or _http_client.is_closed:
        _http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(
                connect=5.0,
                read=10.0,
                write=10.0,
                pool=5.0,
            ),
            limits=httpx.Limits(
                max_connections=10,
                max_keepalive_connections=5,
                keepalive_expiry=30,
            ),
        )
    return _http_client


# Graceful shutdown hook (important on Railway redeploy)
async def close_http_client():
    global _http_client
    if _http_client and not _http_client.is_closed:
        await _http_client.aclose()
        _http_client = None    


# Get result from response: product, language
def get_result(text = None) -> dict:
    blank = {"success": True, "lang": "ru", "product": None, "id": None}
    error = {"success": False}
    # text not exists -> error
    if not text:
        return error
    try:
         # response: language,product - example: nut-100,eng
        items = text.strip().split(",")
        if len(items) > 1:
            return {
                "success": True, 
                "product": items[0],
                "lang": items[1],
                }
        else:
            log(f"202 but failed to decode: {e}")
            return  blank
    except Exception as e:
        log(f"202 but failed to decode: {e}")
        return blank


# Send data to server
async def send_to_backend(data: dict[str, str], text: str) -> dict:
    # sign API_KEY with str using SHA1
    signature = hmac.new(
        BACKEND_KEY.encode("utf-8"),
        hashlib.sha1 # encoding method
    ).hexdigest()

    client = get_http_client()

    for attempt, delay in enumerate(DELAYS, start=1):
        # set up a delay, if specified in current item
        if delay > 0:
            await asyncio.sleep(delay)
        try:
            response = await client.post(
                BACKEND_URL, 
                json=data,
                headers={"X-MHNM-API": signature}
                )
            log(f"Sent #{attempt}: status {response.status_code}")                
            if response.status_code == 202:
                return get_result(response.text) # 202 -> success
            else:
                return get_result(None) # other codes -> error
        
        except Exception as e:
            log(f"Sent attempt #{attempt}: Exception {e}")

    log("Error: Backend did not return 202 after {DELAYS.count} attempts.")
    return {"success": False}
