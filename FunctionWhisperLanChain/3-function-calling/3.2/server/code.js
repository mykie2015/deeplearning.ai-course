export function kelvinToCelsius(kelvin) {
  return JSON.stringify(Math.round(kelvin - 273.15));
}

function geoCode(location) {
  const loc = location.split(",")[0];

  return new Promise(async (resolve, reject) => {
    try {
      const coordinates = await fetch(
        `http://api.openweathermap.org/geo/1.0/direct?q=${loc}&appid=${process.env.WEATHER_API_KEY}`
      );
      const json = await coordinates.json();
      const lat = json[0]?.lat;
      const lon = json[0]?.lon;
      resolve({ lat, lon });
    } catch (err) {
      console.log(err);
    }
  });
}

async function getCurrentWeather(location, unit = "fahrenheit") {
  console.log(location);
  const { lat, lon } = await geoCode(location);
  console.log(lat, lon);
  const response = await fetch(
    `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${process.env.WEATHER_API_KEY}`
  );

  const json = await response.json();
  const currentTemp = json.main.temp;
  const description = json.weather[0].description;

  const weatherInfo = {
    location: location,
    temperature: kelvinToCelsius(currentTemp),
    unit: unit,
    forecast: description,
  };
  return JSON.stringify(weatherInfo);
}
