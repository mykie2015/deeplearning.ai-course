# Add your utilities or helper functions to this file.

import os
from dotenv import load_dotenv, find_dotenv

# these expect to find a .env file at the directory above the lesson.                                                                                                                     # the format for that file is (without the comment)                                                                                                                                       #API_KEYNAME=AStringThatIsTheLongAPIKeyFromSomeService                                                                                                                                     
def load_env():
    _ = load_dotenv(find_dotenv())

def get_openai_api_key():
    load_env()
    openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    return openai_api_key


def get_api_version():
    load_env()
    return os.getenv("OPENAI_API_VERSION")

def get_openai_endpoint():
    load_env()
    return os.getenv("AZURE_OPENAI_ENDPOINT")


