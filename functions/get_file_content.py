import os
from google.genai import types

# This tells the LLM how to use the function
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents and return contents as string, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read the file from, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

# Check if the absolute file path starts with the absolute working directory path
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

# Checks to see if filepath is a file
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

#Read file and return contents as string
    try:
        with open(abs_file_path, 'r') as file:
            content = file.read()
            if len(content) > 10000:
                truncated_content = content[:10000]
                truncation_message = f"[{truncated_content} \"{file_path}\" truncated at 10000 characters]"
                return truncation_message
            else:
                return content
    except Exception as e:
        return f"An error occurred: {e}"
