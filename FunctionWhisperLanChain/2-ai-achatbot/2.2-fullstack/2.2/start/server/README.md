## REST API

....

- **express**: Node.js framework to create and run a Node server
- **nodemon**: tool to restart the server automatically on file changes
- **cors middleware**: allows you to configure and manage an HTTP server to access resources from the same domain
- **openai**: This library provides convenient access to the OpenAI REST API from TypeScript or JavaScript

## Set up environment :

`npm init -y`

## Installation :

`npm i express nodemon cors openai`

## Start the project :

`npm start`

### Send a POST request : send a prompt

```
curl -X POST \
  http://localhost:5000/ask \
  -H 'Content-Type: application/json' \
  -d '{ "input": "Hello, World" }'
```
