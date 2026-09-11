import pandas as pd
import plotly.express as px
import requests

# 1. Expanded Mediterranean and global cities dictionary
cities = {
    # Mediterranean Hubs
    "Sousse": {"lat": 35.8256, "lon": 10.6369, "Country": "Tunisia"},
    "Tunis": {"lat": 36.8065, "lon": 10.1815, "Country": "Tunisia"},
    "Rome": {"lat": 41.9028, "lon": 12.4964, "Country": "Italy"},
    "Athens": {"lat": 37.9838, "lon": 23.7275, "Country": "Greece"},
    "Barcelona": {"lat": 41.3851, "lon": 2.1734, "Country": "Spain"},
    "Istanbul": {"lat": 41.0082, "lon": 28.9784, "Country": "Turkey"},
    "Cairo": {"lat": 30.0444, "lon": 31.2357, "Country": "Egypt"},
    # Other Global References
    "Paris": {"lat": 48.8566, "lon": 2.3522, "Country": "France"},
    "Tokyo": {"lat": 35.6762, "lon": 139.6503, "Country": "Japan"},
    "New York": {"lat": 40.7128, "lon": -74.0060, "Country": "USA"},
    "Sydney": {"lat": -33.8688, "lon": 151.2093, "Country": "Australia"},
    "Reykjavik": {"lat": 64.1466, "lon": -21.9426, "Country": "Iceland"},
}

latitudes = ",".join(str(info["lat"]) for info in cities.values())
longitudes = ",".join(str(info["lon"]) for info in cities.values())

# 2. Shift date range to start from June 2026
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": latitudes,
    "longitude": longitudes,
    "start_date": "2026-06-01",
    "end_date": "2026-09-01",
    "daily": "temperature_2m_mean",
    "timezone": "auto",
}

response = requests.get(url, params=params)
data = response.json()

all_city_data = []
results = data if isinstance(data, list) else [data]
city_names = list(cities.keys())

for i, city_data in enumerate(results):
    city_name = city_names[i]
    info = cities[city_name]
    daily = city_data.get("daily", {})

    temps = daily.get("temperature_2m_mean", [])
    valid_temps = [t for t in temps if t is not None]
    mean_temp = sum(valid_temps) / len(valid_temps) if valid_temps else 0

    all_city_data.append(
        {
            "City": city_name,
            "Country": info["Country"],
            "Latitude": info["lat"],
            "Longitude": info["lon"],
            "Mean_Temp": round(mean_temp, 1),
        }
    )

df_map = pd.DataFrame(all_city_data)
df_map.to_csv("global_weather_map_data.csv", index=False)

# 3. Generate updated interactive map
fig = px.scatter_geo(
    df_map,
    lat="Latitude",
    lon="Longitude",
    text="City",
    color="Mean_Temp",
    size="Mean_Temp",
    hover_name="City",
    hover_data=["Country", "Mean_Temp"],
    color_continuous_scale="Viridis",
    projection="natural earth",
    title="Mediterranean & Global Mean Temperature Map (June - September 2026)",
)

fig.update_layout(
    title_font=dict(size=18, family="Arial", color="#1e293b"),
    geo=dict(showland=True, landcolor="#f1f5f9"),
)

fig.write_html("global_weather_map.html")
print("Updated Mediterranean map saved as global_weather_map.html successfully!")