import OpenAI from "openai";
import fetch from "node-fetch";
import dotenv from "dotenv";

dotenv.config();

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// convert kelvin to celsius
export function kelvinToCelsius(kelvin) {
  return JSON.stringify(Math.round(kelvin - 273.15));
}

// convert kelvin to fahrenheit
export function kelvinToFahrenheit(kelvin) {
  return Math.round(((kelvin - 273.15) * 9) / 5 + 32);
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

async function getCurrentWeather(location, unit) {
  console.log(unit);
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
    temperature:
      unit === "fahrenheit"
        ? kelvinToFahrenheit(currentTemp)
        : kelvinToCelsius(currentTemp),
    unit: unit,
    forecast: description,
  };
  return JSON.stringify(weatherInfo);
}

const functions = [
  {
    name: "get_current_weather",
    description: "Get the current weather in a given location",
    parameters: {
      type: "object",
      properties: {
        location: {
          type: "string",
          description: "The city and state, e.g. San Francisco, CA",
        },
        unit: { type: "string", enum: ["celsius", "fahrenheit"] },
      },
      required: ["location", "unit"],
    },
  },
];

// function here
export default async function askChatbot(req, res) {
  const messages = req.body.messages;
  try {
    const response = await openai.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: messages,
      functions: functions,
      function_call: "auto", // auto is default, but we'll be explicit
    });
    const responseMessage = response.choices[0].message;

    if (responseMessage.function_call) {
      console.log("function called", responseMessage.function_call);
      const availableFunctions = {
        get_current_weather: getCurrentWeather,
      }; // only one function in this example, but you can have multiple
      const functionName = responseMessage.function_call.name;
      const functionToCall = availableFunctions[functionName];
      const functionArgs = JSON.parse(responseMessage.function_call.arguments);
      const functionResponse = await functionToCall(
        functionArgs.location,
        functionArgs.unit
      );

      // Step 4: send the info on the function call and function response to GPT
      messages.push(responseMessage); // extend conversation with assistant's reply
      messages.push({
        role: "function",
        name: functionName,
        content: functionResponse,
      }); // extend conversation with function response

      const secondResponse = await openai.chat.completions.create({
        model: "gpt-3.5-turbo",
        messages: messages,
      }); // get a new response from GPT where it can see the function response

      const filtered_messages = messages
        .filter((message) => message.role !== "function")
        .filter((message) => !!message.content);
      return res.status(200).send({
        messages: [...filtered_messages, secondResponse.choices[0].message],
      });
    } else {
      return res.status(200).send({
        messages: [...messages, responseMessage],
      });
    }
  } catch (err) {
    console.log(err);
    res.status(500).json({ error: "Something went wrong" + err });
  }
}
