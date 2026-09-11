import openmeteo_requests
import requests_cache
from retry_requests import retry
from location_extractor import get_coordinates


cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)


def get_weather_forecast(location="zurich", hours=6):
	coordinates = get_coordinates(location)
	latitude = coordinates['latitude']
	longitude = coordinates['longitude']


	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": latitude,
		"longitude": longitude,
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




	# Structured JSON version of the same data, trimmed to the next `hours` hours,
	# for use as a LangChain tool return value.
	hourly_data = []
	for i in range(min(hours, len(hourly_temperature_2m))):
		hourly_data.append({
			"hour_offset": i,
			"temperature_2m": float(hourly_temperature_2m[i]),
			"relative_humidity_2m": float(hourly_relative_humidity_2m[i]),
			"dew_point_2m": float(hourly_dew_point_2m[i]),
			"rain": float(hourly_rain[i]),
			"showers": float(hourly_showers[i]),
			"snowfall": float(hourly_snowfall[i]),
			"snow_depth": float(hourly_snow_depth[i]),
			"precipitation": float(hourly_precipitation[i]),
		})

	return {
		"location": location,
		"latitude": response.Latitude(),
		"longitude": response.Longitude(),
		"elevation_m": response.Elevation(),
		"hourly_forecast": hourly_data,
	}


if __name__ == "__main__":
	import json
	print(json.dumps(get_weather_forecast("zurich", hours=6), indent=2))