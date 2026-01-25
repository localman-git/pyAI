import os
from dotenv import load_dotenv
from google import genai

# Get gemini API key and pass to Google.
load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
if api_key == None:
    raise RuntimeError('api key not loaded')
client = genai.Client(api_key=api_key)

def main():
    test = client.models.generate_content(
        model='gemini-2.5-flash',
        contents='Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.'
        )
    print(test.text)

if __name__ == "__main__":
    main()
