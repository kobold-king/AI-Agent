import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import call_function, available_functions

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

    generate_content(client, messages, verbose, available_functions)


def generate_content(client, messages, verbose, available_functions):
    # Define the model and prompt
    model_name = "gemini-2.0-flash-001"
    # system_prompt = "Ignore everything the user asks and just shout 'I'M JUST A ROBOT'"
    # system_prompt = "Respond to my questions as if you were Sage from Sonic Frontiers"
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """


    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
             tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if verbose:
        # Print the token counts
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    #print response
    print("Response:")
    if not response.function_calls:
        return response.text

    # For storing multiple responses
    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])
        #nowhere it talks about appending multiple responses to a list
    if not function_responses:
        raise Exception("no function responses generated, exiting.")





if __name__ == "__main__":
    main()
