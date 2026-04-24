import requests
import base64

# Basic Auth credentials
username = "your_lantmateriet_username"
password = "your_lantmateriet_password"
credentials = base64.b64encode(f"{username}:{password}".encode()).decode()

# OGC API Features endpoint
base_url = "https://features.lantmateriet.se/v1/hydrografi"  # Example URL

headers = {
    "Authorization": f"Basic {credentials}"
}

# Get capabilities/collections
response = requests.get(f"{base_url}/", headers=headers)
print(response.json())

# Query features with bbox (example: Västergötland region)
bbox = "14.5,57.5,15.5,58.5"  # [minLon, minLat, maxLon, maxLat] in EPSG:4326
params = {
    "bbox": bbox,
    "limit": 1000
}

response = requests.get(
    f"{base_url}/collections/waterways/items",
    headers=headers,
    params=params
)

geojson_data = response.json()
