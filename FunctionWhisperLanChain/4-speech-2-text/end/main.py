from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
from dotenv import load_dotenv
import os
from handlers import downloadFile, transcribe

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/transcribe")
async def process(request: Request):
    _input = await request.json()
    downloadFile(_input["url"])
    transcript = transcribe()
    return transcript
