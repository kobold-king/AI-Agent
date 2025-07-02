import os
from google.genai import types

# This tells the LLM how to use the function
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory=None):
    abs_working_directory = os.path.abspath(working_directory)
    target_dir = abs_working_directory

    #Checks to see if the path is in the directory and nowhere else
    #This prevents LLM from looking everywhere for the filepath
    if directory:
        target_dir = os.path.abspath(os.path.join(working_directory, directory))

    if not target_dir.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    contents = os.listdir(target_dir)
    output_string = ""

    try:
        for item in contents:
            item_path = os.path.join(target_dir, item)

            if os.path.isfile(item_path):
                file_size = os.path.getsize(item_path)
                output_string += f"- {item}: file_size={file_size} bytes, is_dir=False\n"
            elif os.path.isdir(item_path):
                file_size = os.path.getsize(item_path)
                output_string += f"- {item}: file_size={file_size} bytes, is_dir=True\n"
                output_string += get_files_info(working_directory, item_path)

    except Exception as e:
        return f"Error listing files: {e}"

    return output_string
