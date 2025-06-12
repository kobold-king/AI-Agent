import os
import sys
from dotenv import load_dotenv
from google import genai

# Load environment variables from a .env file
load_dotenv()

# Initialize the Google GenAI client
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

#Command Line prompt
if len(sys.argv) > 1:
    prompt = str(sys.argv[1:])
    print(f"Using prompt: {prompt}")
else:
    print("No prompt provided.")
    sys.exit(1)


# Define the model and prompt
model = "gemini-2.0-flash-001"
contents = prompt

# Get a response from the model
response = client.models.generate_content(
    model=model, contents=contents
)

# Print the response
print(response.text)

if response.usage_metadata:
    # Print the token counts
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
