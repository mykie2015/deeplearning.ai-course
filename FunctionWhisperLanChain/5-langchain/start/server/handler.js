import fetch from "node-fetch";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { dirname } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export default async function (url) {
  console.log("Downloading audio...");
  try {
    const response = await fetch(url);
    const buffer = await response.buffer();
    const filePath = path.join(__dirname, "media", "audio.mp3");

    // Ensure the media directory exists
    const dirPath = path.join(__dirname, "media");
    if (!fs.existsSync(dirPath)) {
      fs.mkdirSync(dirPath);
    }

    fs.writeFileSync(filePath, buffer);
    console.log("Audio file has been downloaded and saved as audio.mp3");
  } catch (error) {
    console.error(`Error downloading file: ${error}`);
  }
}
