import os
from google.genai import types


def get_files_info(working_directory, directory="."):

    try:

        full_path = os.path.abspath(os.path.join(working_directory, directory))

        # Security check: ensure the path stays within working_directory
        working_abs = os.path.abspath(working_directory)
        if not full_path.startswith(working_abs):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if path is a directory
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        

        # List directory contents
        items = os.listdir(full_path)
        if directory == ".":
            result_lines = ['Result for current directory:']
        else:
            result_lines = [f"Result for {directory} directory:"]
        for item in items:
            item_path = os.path.join(full_path, item)
            file_size = os.path.getsize(item_path) if os.path.isfile(item_path) else 0
            is_dir = os.path.isdir(item_path)
            result_lines.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")

        # Join results into a single string
        return "\n".join(result_lines)
    except Exception as e:
        return f"Error: {str(e)}"

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




if __name__ == "__main__":
    get_files_info('.')