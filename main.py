import requests
from twilio.rest import Client


# ================== extracting data from the api ================= #

latitude = 40.712776
longitude = -74.005974

OWM_endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = "SECRET WEATHER API KEY"

# lat on lon for NYC
weather_params = {
    "lat": 40.712776,
    "lon": -74.005974,
    "units": "metric",
    "appid": api_key,
    "exclude": "current,minutely,daily",
}

response = requests.get(url=OWM_endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

id = weather_data["hourly"][0]["weather"][0]["id"]
weather_slice = weather_data["hourly"][:16]


# ================== Telling if will rain ================= #

will_rain = False
list_of_id = []
for i in weather_slice:
    id = i["weather"][0]["id"]
    if int(id) < 700:
        will_rain = True

rain_alert = ""
if will_rain:
    rain_alert = "Take an umbrella!"
if not will_rain:
    rain_alert = "No rain today"


# ================== Telling the weather ================= #

list_of_temps = []
for i in weather_data["hourly"]:
    temp = i["temp"]
    list_of_temps.append(temp)
real_list_of_temps = list_of_temps[:15:3]
# print(real_list_of_temps)


# ================== list of icons ================= #

list_descriptions = []
for i in weather_data["hourly"]:
    description = i["weather"][0]["main"]
    list_descriptions.append(description)
# print(list_descriptions)

real_list_descriptions = list_descriptions[:15:3]
# print(real_list_descriptions)

list_of_icons = []
for n in real_list_descriptions:
    if n == "Clear":
        list_of_icons.append("☀️🌞️")
    elif n == "Clouds":
        list_of_icons.append("☁️️")
    elif n == "Rain" or n == "Drizzle":
        list_of_icons.append("🌧☔️")
    elif n == "Thunderstorm":
        list_of_icons.append("🌩⚡️")
    elif n == "Snow":
        list_of_icons.append("❄️☃️️")
    elif n == "Mist":
        list_of_icons.append("🌫")
    else:
        list_of_icons.append("")


# ================== creating final message ================= #

if list_of_icons[3] == "☀️🌞️":
    list_of_icons[3] = "☁️️"
if list_of_icons[4] == "☀️🌞️":
    list_of_icons[4] = "☁️️"
temps_text = f"6:00 - {int(real_list_of_temps[0])} {list_of_icons[0]}\n" \
             f"10:00 - {int(real_list_of_temps[1])} {list_of_icons[1]}\n" \
             f"14:00 - {int(real_list_of_temps[2])} {list_of_icons[2]}\n" \
             f"18:00 - {int(real_list_of_temps[3])} {list_of_icons[3]}\n" \
             f"22:00 - {int(real_list_of_temps[4])} {list_of_icons[4]}"

good_day = "Have a great day!! ❤️"
print(f"{rain_alert}\n{temps_text}\n{good_day}")


# ================== Sending the message ================= #

account_sid = "SECRET TWILIO ACCOUNT SID"
auth_token = "SECRET AUTH TOKEN"

client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body=f"{rain_alert}\n{temps_text}\n{good_day}",
                     from_='PHONE NUMBER',
                     to='PHONE NUMBER'
                 )

print(message.status)

print(weather_data["hourly"])
