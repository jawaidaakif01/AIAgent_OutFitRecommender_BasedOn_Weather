import json
import requests

NOMINATIM_URL =   "https://nominatim.openstreetmap.org/search"


def get_coordinates(location: str) -> dict:
    """
    Geocode a place name into lat/lon using OpenStreetMap Nominatim.
    Raises ValueError if the location can't be found or the request fails.
    """
    try:
        params = {"q": location, "format":"jsonv2"}
        headers = {"User-Agent": "WeatherApp_LearningProject/1.0 (aakif.dev@gmail.com)"}
        r = requests.get(url=NOMINATIM_URL, params=params, headers=headers)
        if r.status_code==200:
            # print("success")
            data = r.json()
            latitude = data[0]['lat']
            longitude = data[0]['lon']

            coordinates = {
                'latitude':latitude,
                'longitude':longitude
            }

            # print(coordinates)
            return coordinates

    except Exception as e:
        return e