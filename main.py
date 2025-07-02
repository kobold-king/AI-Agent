import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info


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

    # List of available functions we have made declarations/schema for
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
)
    generate_content(client, messages, verbose, available_functions)


    # Get a response from the model
def generate_content(client, messages, verbose, available_functions):
    # Define the model and prompt
    model_name = "gemini-2.0-flash-001"
    # system_prompt = "Ignore everything the user asks and just shout 'I'M JUST A ROBOT'"
    # system_prompt = "Respond to my questions as if you were Sage from Sonic Frontiers"
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

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

    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")

    # Old Harder to read code
    # if response.candidates[0].content.parts[0].function_call:
    #     function_call_part = response.candidates[0].content.parts[0].function_call
    #     print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    # else:
    #     print(response.text)

if __name__ == "__main__":
    main()
