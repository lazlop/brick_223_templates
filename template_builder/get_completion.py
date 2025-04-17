# MODEL = "openai/gpt-4o"
MODEL = "anthropic/claude-sonnet"
# MODEL = "google/gemini-pro"
import openai # CBORG API Proxy Server is OpenAI-compatible through the openai module
import yaml
with open('/Users/lazlopaul/Desktop/cborg/api_key.yaml', 'r') as file:
    config = yaml.safe_load(file)
    API_KEY = config['key']
    BASE_URL = config['base_url']

client = openai.OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

def get_completion(prompt, system_prompt = None):
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]
    if system_prompt:
        messages.append(
            {
                "role": "system",
                "content":system_prompt
            }
        )
    response = client.chat.completions.create(
            model=MODEL, 
            messages = messages,
            temperature=0.0  
        )

    return response.choices[0].message.content