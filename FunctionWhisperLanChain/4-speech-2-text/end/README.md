## Create a virtual environment :

```
python -m venv env
```

## Activate the virtual environment :

```
source env/bin/activate
```

## [get an key](https://platform.openai.com/account/api-keys)

`export OPENAI_API_KEY=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`

## Installation:

### install requirements :

use `pip3 on a mac`
`pip install -r requirements.txt`

### install whisper model

`pip install git+https://github.com/openai/whisper.git`

### install ffmpeg (requirements for the whisper library)

#### On macOS:

`brew install ffmpeg`

#### On Ubuntu:

```
sudo apt update
sudo apt install ffmpeg

```

#### On Windows:

Download the executable from the [official FFmpeg site](https://ffmpeg.org/download.html)

### install server [uvicorn ASGI server](https://www.uvicorn.org/)

`pip install "uvicorn[standard]"`

## Start the server:

`uvicorn main:app --reload`

## Start the server:

<!--
pick a sample from here:
https://www.thepodcastexchange.ca/audio-samples
-->

```
curl -X POST \
  http://127.0.0.1:8000/transcribe \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "https://www.thepodcastexchange.ca/s/AD-CONAF-2019BC-MID-JPWiser-v2-1.mp3"
  }'
```
