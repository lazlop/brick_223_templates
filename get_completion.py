MODEL = "openai/gpt-4o"
# MODEL = "google/gemini-pro"
import openai # CBORG API Proxy Server is OpenAI-compatible through the openai module
import yaml
with open('/Users/lazlopaul/Desktop/cborg/api_key.yaml', 'r') as file:
    API_KEY= yaml.safe_load(file)['key']

client = openai.OpenAI(
    api_key=API_KEY,
    base_url="https://api.cborg.lbl.gov" # Local clients can also use https://api-local.cborg.lbl.gov
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
            temperature=0.0   # Optional: set model temperature to control amount of variance in response
        )

    return response.choices[0].message.content