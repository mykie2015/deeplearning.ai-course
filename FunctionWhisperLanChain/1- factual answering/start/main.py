import openai


# Set up the OpenAI API client


# Set up the model and prompt


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
    print(instructions)


if __name__ == "__main__":
    start()
