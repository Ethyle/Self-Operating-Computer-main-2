# config.py
import os
from dotenv import load_dotenv
import platform
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")

if OPENAI_API_KEY is None:
    raise EnvironmentError(
        "The OpenAI API key is not defined. Please set the OPENAI_API_KEY environment variable."
    )

if REPLICATE_API_TOKEN is None:
    raise EnvironmentError(
        "The Replicate API token is not defined. Please set the REPLICATE_API_TOKEN environment variable."
    )

os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# OS Detection
CURRENT_OS = platform.system().lower()

# Initialize OpenAI client
CLIENT = OpenAI(api_key=OPENAI_API_KEY)
