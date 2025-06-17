import os

def get_files_info(working_directory, directory=None):
    abs_directory = os.path.abspath(directory)
    abs_working_directory = os.path.abspath(working_directory)

    #Checks to see if the path is in the directory and nowhere else
    #This prevents LLM from looking everywhere for the filepath
    if not abs_directory.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'

    contents = os.listdir(directory)
    output_string = ""

    try:
        for item in contents:
            item_path = os.path.join(directory, item)
            file_size = os.path.getsize(file_path)

            if os.path.isfile(item_path):
                file_size = os.path.getsize(file_path)
                output_string += f"- {item}: file_size={file_size} bytes, is_dir=False\n"
            elif os.path.isdir(item_path):
                output_string += f"- {item}: file_size={file_size} bytes, is_dir=True\n"
                output_string += get_files_info(working_directory, item_path)

    except Exception as e:
        return f'Error: "{e}"'

    return output_string
