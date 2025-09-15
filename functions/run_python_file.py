import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Security check: ensure the path stays within working_directory
        working_abs = os.path.abspath(working_directory)
        if not full_path.startswith(working_abs):
            return f'Cannot execute "{file_path}" as it is outside'
        
        # Check if path is a file
        if not os.path.isfile(full_path):
            return f'File "{file_path}" not found'
        
        # Check extension
        if not full_path.endswith(".py"):
            return f'"{file_path}" is not a Python file'

        # Run the Python file with uv
        result = subprocess.run(
            ["uv", "run", full_path] + args,
            cwd=working_abs,
            capture_output=True,
            text=True,
            timeout=30
        )

        output_parts = []

        if result.stdout.strip():
            output_parts.append(f"STDOUT:\n{result.stdout.strip()}")
        if result.stderr.strip():
            output_parts.append(f"STDERR:\n{result.stderr.strip()}")

        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if not output_parts:
            return "No output produced."

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
