## LangChain

....

Documentation :

- [Open AI Whisper Audio](https://js.langchain.com/docs/modules/data_connection/document_loaders/integrations/file_loaders/)
- [Open AI Chat models](https://js.langchain.com/docs/modules/model_io/models/chat/integrations/openai)
- [Summarization Chain](https://js.langchain.com/docs/modules/chains/popular/summarize)

## Dependencies :

- **langchain**: LangChain is written in TypeScript and provides type definitions for all of its public APIs.
- **dotenv**: module to load environment variables from a .env file into process.env
- **node-fetch**: A light-weight module that brings window.fetch to Node.js

## Installation :

`npm install`

`npm install -S langchain`

## Start the project :

`npm start`

## Test the project :

<!--
pick a sample from here:
https://www.thepodcastexchange.ca/audio-samples
-->

localhost:5000

```
curl -X POST \
  http://localhost:5000/transcribe \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "https://www.thepodcastexchange.ca/s/Allusionist-HSBC-PRE-2019-07-12.mp3"
  }'
```
