# MODEL = "openai/gpt-4.1" # Unsure on performance, more expesnvie
# MODEL = "anthropic/claude-sonnet" # Best, most expesnvie 
# MODEL = "lbl/cborg-chat:latest" # Free
# MODEL = "lbl/cborg-coder:latest" # Free, least compute
MODEL = "lbl/llama" # Free
# MODEL = "google/gemini-flash-exp" # Free during experiment, temporary
# MODEL = "google/gemini-flash" # Cheapest tokens
# MODEL = "anthropic/claude-haiku" # More expensive, less performant than gemeni

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