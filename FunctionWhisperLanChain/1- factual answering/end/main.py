import os
import openai
from colorama import Fore
from dotenv import load_dotenv

load_dotenv()

# Load the environment variables - set up the OpenAI API client
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up the model and prompt
LANGUAGE_MODEL = "gpt-3.5-turbo-instruct"
PROMPT_TEST = "Say this is a test"


def start():
    print("MENU")
    print("====")
    print("[1]- Ask a question")
    print("[2]- Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        ask()
    elif choice == "2":
        exit()
    else:
        print("Invalid choice")
        start()


def ask():
    instructions = (
        "Type your question and press ENTER. Type 'x' to go back to the MAIN menu.\n"
    )
    print(Fore.BLUE + "\n\x1B[3m" + instructions + "\x1B[0m" + Fore.RESET)
    while True:
        print(Fore.WHITE + "-------------------------------------------------\n")
        user_input = input("Q: ")
        # Exit
        if user_input == "x":
            start()
        else:
            # Generate a response
            completion = openai.Completion.create(
                model="gpt-3.5-turbo-instruct",
                prompt="Q: " + str(user_input),
                temperature=0,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )

            response = completion.choices[0].text.replace("\n", "").replace("\r", "")

            print(Fore.BLUE + response + Fore.RESET)


if __name__ == "__main__":
    start()
