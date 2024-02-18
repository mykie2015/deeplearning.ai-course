// import
import dotenv from "dotenv";
import { fileURLToPath } from "url";
import path, { dirname } from "path";
import download from "./handler.js";

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// OpenAI  models

// OpenAI Whisper Audio

export default async (req, res) => {
  await download(req.body.url);
  console.log("Transcribing audio...");
};
