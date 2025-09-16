from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file
from google.genai import types


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_dictionary = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_file": write_file,
        "run_python_file": run_python_file
    }

    if function_call_part.name not in function_dictionary:
        return types.Content(role="tool",
                             parts=[types.Part.from_function_response(name=function_call_part.name,
                                                                      response={"error": f"Unknown function: {function_call_part.name}"},
        )
    ],)


    function = function_dictionary[function_call_part.name]

    reponse = function(working_directory="./calculator", **function_call_part.args)

    return types.Content(role="tool",
                         parts=[types.Part.from_function_response(name=function_call_part.name,
                                                                  response={"result": reponse},
        )
    ],)

if __name__ == "__main__":
    call_function()