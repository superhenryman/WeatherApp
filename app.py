from flask import Flask, render_template, request
import requests
key = "9752642c35c446089b121331252401"
def GetWeather(city):
    print(city)
    url = f"https://api.weatherapi.com/v1/current.json?key={key}&q={city}"
    response = requests.get(url)
    if response.status_code == 400:
        return "Error!"
    return response.json()
def ReturnShit(weather_items):
    # Mapping of old names to new names
    map = {
        "temp_c": "Temperature in Celsius",
        "humidity": "Humidity percentage",
        "precip_mm": "Preceptation Milimeters",
        "wind_kph": "Wind's speed in KPH",
        "wind_dir": "Wind direction",
        "vis_km": "Kilometers visible",
        "uv": "UV Light",
        "gust_kph": "Rush of wind",
        "wind_degree": "Wind degree",
        "feelslike_c": "Feels like celsius",
        "temp_f": "Temperature in Farenheit",

    }
    
    weather_data = {}
    for key, value in weather_items:
        if key in ["last_updated_epoch", "last_updated", "temp_f", "cloud", "pressure_in"
                   , "pressure_out", "precip_in", "windchill_c", "windchill_f", "heatindex_c", "heatindex_f", "dewpoint_c", "condition", "dewpoint_f", "gust_mph", "vis_miles",
                   "feelslike_f", "dewpoint_f", "pressure_mb", "wind_mph"]:
            continue
        # rename the key if it exists in the mapping
        new_key = map.get(key, key)  # use the original key if no mapping exists
        weather_data[new_key] = value
    return weather_data
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form.get("city")
        response = GetWeather(city)
        if response == "Error!":
            # Rickroll the user for putting a wrong city.
            return render_template("jumper.html")
        currentweather = response["current"]
        tuple_current = tuple(currentweather.items())
        currenttextcondition = currentweather["condition"]["text"]
        weather_data = ReturnShit(tuple_current)
        return render_template("index.html", weather=weather_data, condition=currenttextcondition)
    return render_template("index.html")
if  __name__ == "__main__":
    app.run(debug=True)