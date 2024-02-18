# Chatbot API - Function Calling

---

### Node

- #### Node installation on Windows

  Just go on [official Node.js website](https://nodejs.org/) and download the installer.
  Also, be sure to have `git` available in your PATH, `npm` might need it (You can find git [here](https://git-scm.com/)).

- #### Node installation on Ubuntu

  You can install nodejs and npm easily with apt install, just run the following commands.

      $ sudo apt install nodejs
      $ sudo apt install npm

- #### Other Operating Systems
  You can find more information about the installation on the [official Node.js website](https://nodejs.org/) and the [official NPM website](https://npmjs.org/).

If the installation was successful, you should be able to run the following command.

    $ node --version
    v8.11.3

    $ npm --version
    6.1.0

If you need to update `npm`, you can make it using `npm`! Cool right? After running the following command, just open again the command line and be happy.

    $ npm install npm -g

###

### Yarn installation

After installing node, this project will need yarn too, so just run the following command.

      $ npm install -g yarn

---

### [1]- Download starter project

#### [1.1] - Install libraries

`npm i express nodemon cors dotenv openai`

- **dotenv**: module to load environment variables from a `.env` file
- **express**: Node.js framework to create and run a Node server
- **nodemon**: tool to restart the server automatically on file changes
- **cors**: middleware to handle requests from different origins
- **openai**: Node.js library to make requests to completion APIs and language models
- **node-fetch**: library to make requests to external APIs
- **babel**: transpiler to convert ES6+ code to ES5

#### [1.2] Add an API KEY - [Api Keys](https://platform.openai.com/account/api-keys)

inside the **.env** file, add your unique key

```
# your unique API key value goes here
OPENAI_API_KEY=sk-############

```

#### [1.3] Start the project

`npm start`
