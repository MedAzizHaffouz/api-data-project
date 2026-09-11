import requests
import pandas as pd
import matplotlib.pyplot as plt

url = "https://api.open-meteo.com/v1/forecast?latitude=35.8256&longitude=10.6369&current_weather=true"
response = requests.get(url)
data = response.json()

weather_info = data["current_weather"]
df = pd.DataFrame([weather_info])
df.to_csv("clean_data.csv", index=False)

# Create a quick bar chart of temperature vs windspeed
plt.figure(figsize=(6, 4))
plt.bar(['Temperature (°C)', 'Windspeed (km/h)'], [df['temperature'][0], df['windspeed'][0]], color=['orange', 'skyblue'])
plt.title('Current Weather Metrics')
plt.savefig('weather_chart.png')
print("Chart saved as weather_chart.png successfully!")