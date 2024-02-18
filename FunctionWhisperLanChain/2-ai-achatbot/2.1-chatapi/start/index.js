require("dotenv").config();
const readline = require("readline").createInterface({
  input: process.stdin,
  output: process.stdout,
});

// Import Open AI

// Open AI configuration

async function main() {
  console.log("\n\n----------------------------------");
  console.log("          CHAT WITH AI 🤖   ");
  console.log("----------------------------------");
  console.log("type 'x' to exit\n");
  runConversation();
}

async function runConversation() {
  readline.question("You :", (input) => {
    if (input.split().includes("x")) {
      console.log("END OF CHAT");
      process.exit();
    }
    // API call here

    readline.close();
  });
}
main();
