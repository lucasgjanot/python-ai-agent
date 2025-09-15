import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from functions.schemas import *
from functions.call_function import call_function

def main():

    try:

        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")

        client = genai.Client(api_key=api_key)

        args = sys.argv
        if len(args) == 1:
            print("O programa requer um argumento")
            sys.exit(1)


        user_prompt = sys.argv[1]

        messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]

        system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

        available_functions = types.Tool(function_declarations=[schema_get_files_info,schema_get_file_content,schema_run_python_file,
                                                                schema_write_file])

        response = client.models.generate_content(model="gemini-2.0-flash-001",
                                                contents=messages,
                                                config=types.GenerateContentConfig(tools=[available_functions], 
                                                                                    system_instruction=system_prompt)
                                                )

        
        if response.text:
            print(response.text)

        if response.function_calls:
            for function in response.function_calls:
                call = call_function(function, verbose=True)

        if "--verbose" in  args:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print(f"-> {call.parts[0].function_response.response['result']}")



    except Exception as e:
        return f"Error: {str(e)}"
    
if __name__ == "__main__":
    main()
