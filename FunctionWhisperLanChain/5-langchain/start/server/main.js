import express from "express";
import cors from "cors";
import transcribe from "./summarize.js";
const app = express();

app.use(cors());
app.use(express.json());
const port = process.env.PORT || 5000;

// Endpoint to send a prompt
app.post("/transcribe", transcribe);

app.listen(port, () => console.log(`Server is running on port ${port}!!`));
