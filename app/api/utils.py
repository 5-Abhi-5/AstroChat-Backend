import requests
import os


openai_api_key = os.getenv('OPENAI_API_KEY')
initial_prompt = os.getenv('INITIAL_PROMPT')


'''
Utility Function that sends a request to the OpenAI API to generate a response based on the user's prompt.
'''
def generate_openai_response(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }
 
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    
    else:
        return f"Error: {response.status_code} - {response.text}"
    
    
'''TODO: Implement the function using the user's zodiac sign and user prompt to generate a final prompt.'''
def generate_prompt(user_prompt):
    final_prompt = initial_prompt + " " + user_prompt  #Dummy implementation
    return final_prompt