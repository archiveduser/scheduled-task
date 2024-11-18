import json
import requests

ALIST_URL = os.getenv("ALIST_URL", "")
ALIST_USERNAME = os.getenv("ALIST_USERNAME", "")
ALIST_PASSWORD = os.getenv("ALIST_PASSWORD", "")
ALIST_DRIVER_PATH = os.getenv("ALIST_DRIVER_PATH", "")
ALIST_DRIVER_ID = os.getenv("ALIST_DRIVER_ID", "")

content = ""
with open("/tmp/urltree", "r", encoding="utf8") as f:
    content = f.read()

response = requests.post(
    f"{ALIST_URL}/api/auth/login",
    json={"username": f"{ALIST_USERNAME}", "password": f"{ALIST_PASSWORD}"},
)

response.raise_for_status()
token = response.json()["data"]["token"]


response = requests.post(
    f"{ALIST_URL}/api/admin/storage/update",
    headers={"Authorization": token, "Content-Type": "application/json"},
    json={
        "id": int(ALIST_DRIVER_ID),
        "mount_path": ALIST_DRIVER_PATH,
        "driver": "UrlTree",
        "status": "work",
        "addition": json.dumps({"url_structure": alist_tree_text, "head_size": False}),
        "enable_sign": False,
        "order_by": "",
        "order_direction": "",
        "extract_folder": "",
        "web_proxy": False,
    },
)

print(response.json())
