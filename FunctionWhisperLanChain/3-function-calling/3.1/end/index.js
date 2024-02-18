import express from "express";
import cors from "cors";
import ask from "./handlers.js";

const app = express();
app.use(cors());
app.use(express.json());
const port = process.env.PORT || 5000;

app.get("/", async (_, res) => {
  return res.status(200).send("<h1>AI-Chatbot 🤖</h1>");
});

// Endpoint to send a prompts to OpenAI
app.post("/ask", ask);

app.listen(port, () => console.log(`Server is running on port ${port}!!`));
