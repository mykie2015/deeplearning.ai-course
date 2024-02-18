// Import Open AI
const OpenAI = require("openai");
require("dotenv").config();

const readline = require("readline").createInterface({
  input: process.stdin,
  output: process.stdout,
});

const openai = new OpenAI();
const messages = [{ role: "system", content: "You are a helpful assistant." }];

// Open AI configuration

async function main() {
  console.log("\n\n----------------------------------");
  console.log("          CHAT WITH AI 🤖   ");
  console.log("----------------------------------");
  console.log("type 'x' to exit\n");
  runConversation();
}

async function runConversation() {
  readline.question("You :", async (input) => {
    if (input.split().includes("x")) {
      console.log("END OF CHAT");
      process.exit();
    }
    try {
      // API call here
      messages.push({ role: "user", content: input });
      const completion = await openai.chat.completions.create({
        messages: messages,
        model: "gpt-3.5-turbo",
      });
      messages.push(completion.choices[0].message);

      console.log("Bot: " + completion.choices[0].message.content);
      runConversation();
    } catch (error) {
      console.log(error);
    }
  });
}
main();
