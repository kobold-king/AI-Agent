import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
# Load environment variables from a .env file
    load_dotenv()

    # Initialize the Google GenAI client
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    #Command Line prompt
    verbose = "--verbose" in sys.argv

    if len(sys.argv) > 1:
        args = args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    else:
        print("Eggman Empire: Sage AI Assistant")
        print("It appears you forgot your prompt.")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I better serve Dr. Eggman?"')
        sys.exit(1)

    prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    generate_content(client, messages, verbose)


    # Get a response from the model
def generate_content(client, messages, verbose):
    # Define the model and prompt
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    if verbose:
        # Print the token counts
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    #print response
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()
