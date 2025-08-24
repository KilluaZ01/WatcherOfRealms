import requests

BASE_URL = "https://api.airproxy.io"

# Define fallback localhost proxy (or dummy info)
LOCAL_PROXY = {
    "id": None,
    "ip": "127.0.0.1",
    "port": 8888,
    "username": "",
    "password": "",
}

def get_proxy_list(proxy_api, log_func):
    if not proxy_api or proxy_api == "your_proxy_proxy_api":
        print("No valid API key found. Falling back to localhost proxy.")
        return [LOCAL_PROXY] * 5  # Simulate list with multiple localhost entries

    try:
        response = requests.get(
            f"{BASE_URL}/api/proxy/list/",
            params={"key": proxy_api},
            timeout=10
        )
        if response.ok:
            data = response.json()
            proxies = data.get("proxies", [])
            if not proxies:
                print("No proxies found from Airproxy. Using localhost fallback.")
                log_func("Proxies not found. Using localhost fallback.")
                return [LOCAL_PROXY] * 5
            log_func("Proxies found. Using Proxy.")
            return proxies
        else:
            print(f"❌ Failed to fetch proxies from Airproxy: {response.text}")
            return [LOCAL_PROXY] * 5
    except Exception as e:
        print(f"❌ Error contacting Airproxy: {e}")
        return [LOCAL_PROXY] * 5

def rotate_proxy_ip(proxy_api, proxy_id, log_func):
    if not proxy_api or not proxy_id:
        print("Skipping IP rotation — using fallback or localhost proxy.")
        return

    try:
        response = requests.get(
            f"{BASE_URL}/api/proxy/change_ip/",
            params={"key": proxy_api, "id": proxy_id},
            timeout=10
        )
        if response.ok:
            data = response.json()
            print(f"Rotated Proxy {proxy_id} → New IP: {data.get('new_ip')}")
            log_func(f"Rotated Proxy {proxy_id} → New IP: {data.get('new_ip')}")
        else:
            print(f"Failed to rotate proxy: {response.text}")
            log_func('Failed to rotate proxy')
    except Exception as e:
        print(f"Error rotating proxy: {e}")