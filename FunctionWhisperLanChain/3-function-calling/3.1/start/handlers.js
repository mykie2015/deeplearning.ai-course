import OpenAI from "openai";
import fetch from "node-fetch";
import dotenv from "dotenv";

dotenv.config();

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

function kelvinToCelsius(kelvin) {}

function geoCode(location) {}

async function getCurrentWeather(location, unit = "fahrenheit") {}

// function here

export default async function askChatbot(req, res) {
  const completion = await openai.chat.completions.create({
    messages: req.body.messages,
    model: "gpt-3.5-turbo",
  });

  return res.status(200).send({
    messages: [...req.body.messages, completion.choices[0].message],
  });
}
