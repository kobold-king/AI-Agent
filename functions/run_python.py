import os
import subprocess

def run_python_file(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Check if the absolute file path starts with the absolute working directory path
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # Check if file path exists
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    # check if file is a py file
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    # run python
    try:
        result = subprocess.run(["python3", file_path], cwd=abs_working_directory, timeout=30, capture_output=True, text=True)
        print(f"Command executed successfully in {working_directory}:")

        output = f"STDOUT:{result.stdout}\nSTDERR:{result.stderr}"

        if result.returncode != 0:
            output = f"STDOUT:{result.stdout}\nSTDERR:{result.stderr}\nProcess exited with code {result.returncode}"

        if not output:
            return "No output produced."

        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
