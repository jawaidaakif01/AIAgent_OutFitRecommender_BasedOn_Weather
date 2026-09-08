import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry


cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)



url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 28.6214,
	"longitude": 77.2148,
	"hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "rain", "showers", "snowfall", "snow_depth", "precipitation"],
	"models": "ncep_gfs_seamless",
	"forecast_days": 1,
}
responses = openmeteo.weather_api(url, params = params)


response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")


hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
hourly_rain = hourly.Variables(3).ValuesAsNumpy()
hourly_showers = hourly.Variables(4).ValuesAsNumpy()
hourly_snowfall = hourly.Variables(5).ValuesAsNumpy()
hourly_snow_depth = hourly.Variables(6).ValuesAsNumpy()
hourly_precipitation = hourly.Variables(7).ValuesAsNumpy()


with open("data.txt", "a", encoding="utf-8") as f:
    f.write("These are some of the metrices of whether in next 24 hours:\n")
    f.write("\nNext 24 hour temperature data:\n")
    for i in hourly_temperature_2m:
        f.write(f"{i:.1f}°C, ")

    f.write("\nNext 24 hour relative humidity:\n")
    for i in hourly_relative_humidity_2m:
        f.write(f"{i:.1f}%, ")

    f.write("\nNext 24 hour dew point:\n")
    for i in hourly_dew_point_2m:
        f.write(f"{i:.1f}°C, ")

    f.write("\nNext 24 hour rain:\n")
    for i in hourly_rain:
        f.write(f"{i}mm, ")

    f.write("\nNext 24 hour showers:\n")
    for i in hourly_showers:
        f.write(f"{i}mm, ")

    f.write("\nNext 24 hour snowfall:\n")
    for i in hourly_snowfall:
        f.write(f"{i}cm, ")

    f.write("\nNext 24 hour snow depth:\n")
    for i in hourly_snow_depth:
        f.write(f"{i}m, ")

    f.write("\nNext 24 hour precipitation:\n")
    for i in hourly_precipitation:
        f.write(f"{i}mm, ")




