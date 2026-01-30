import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions, call_function

def main():
    
    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')
    if api_key == None:
        raise RuntimeError('api key not loaded')
    client = genai.Client(api_key=api_key)

    model = 'gemini-2.5-flash'

    parser = argparse.ArgumentParser(description='Chatbot')
    parser.add_argument('user_prompt', type=str, help='User prompt')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        
        response = client.models.generate_content(
            model=model,
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions]),
            )

        if not response.usage_metadata:
            raise RuntimeError('no usage metadata returned from api')
        if not response.text and not response.function_calls:
            raise RuntimeError('no text or function calls returned from api')
        
        if args.verbose:
            print(f'User prompt: {args.user_prompt}')
            print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
            print(f'Response tokens: {response.usage_metadata.candidates_token_count}')

        if response.candidates:
            for message in response.candidates:
                messages.append(message.content)

        if response.function_calls:
            function_results = []
            for call in response.function_calls:
                function_call_result = call_function(call, verbose=args.verbose)
                if not function_call_result.parts:
                    raise RuntimeError('no parts list returned from function call')
                if not function_call_result.parts[0].function_response.response:
                    raise RuntimeError('no response returned from function call')
                function_results.append(function_call_result.parts[0])
                messages.append(types.Content(role='user', parts=function_results))
                if args.verbose:
                    print(f'-> {function_call_result.parts[0].function_response.response}')
        else:     
            print(f'Response: {response.text}')
            break

    else:
        sys.exit(1)

if __name__ == "__main__":
    main()