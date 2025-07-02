import os
from google.genai import types

# This tells the LLM how to use the function
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write or overwrite files to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be written to the file."
            ),
        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Check if the absolute file path starts with the absolute working directory path
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

#write and or create file
    try:
        os.makedirs(working_directory, exist_ok=True)
        print(f"Directory '{working_directory}' ensured to exist.")
        file_path = os.path.join(working_directory, file_path)

        with open(file_path, 'w') as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
