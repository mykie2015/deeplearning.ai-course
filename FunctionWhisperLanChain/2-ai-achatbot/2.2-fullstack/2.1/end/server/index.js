const express = require("express");
const OpenAI = require("openai");
require("dotenv").config();
const app = express();
const port = 5000;

app.use(express.json());

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});
const system_message = [
  { role: "system", content: "You are a helpful assistant." },
];

app.get("/", (req, res) => {
  res.send("<h1>AI-Chatbot</h1>");
});

async function askChatbot(req, res) {
  const messages = [
    ...system_message,
    { role: "user", content: req.body.input },
  ];
  const completion = await openai.chat.completions.create({
    messages: messages,
    model: "gpt-3.5-turbo",
  });

  messages.push([...messages, completion.choices[0].message]);

  res.send({ message: "Bot: " + completion.choices[0].message.content });
}

app.post("/ask", askChatbot);

app.listen(port, () => {
  console.log(`Server is up and running ${port}`);
});
