import os

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
