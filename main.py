import os
from dotenv import load_dotenv
from google import genai

def main():
    
    # Get gemini API key and pass to Google.
    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')
    if api_key == None:
        raise RuntimeError('api key not loaded')
    client = genai.Client(api_key=api_key)

    model = 'gemini-2.5-flash'
    contents = 'Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.'
    
    response = client.models.generate_content(model=model,contents=contents)

    if response.usage_metadata == None:
            raise RuntimeError('no usage metadata returned from api')
    if response.text == None:
            raise RuntimeError('no text returned from api')
    
    print(f'User prompt: {contents}')
    print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
    print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
    print(f'Response: {response.text}')

if __name__ == "__main__":
    main()