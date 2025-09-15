import os
from functions.config import MAX_CHARS

def get_file_content(working_directory, file_path):

    try:

        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Security check: ensure the path stays within working_directory
        working_abs = os.path.abspath(working_directory)
        if not full_path.startswith(working_abs):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if path is a file
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

        return file_content_string + f' [...File "{file_path}" truncated at 10000 characters]'

    except Exception as e:
        return f"Error: {str(e)}"