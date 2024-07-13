import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Define the API key and endpoint
api_key = os.getenv("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/chat/completions"

# Set the request headers
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def generate_response(messages):
    # Prepare the data payload
    data = {
        "model": "llama3-8b-8192",
        "messages": messages,
        "temperature": 1,
        "max_tokens": 1024,
        "top_p": 1,
        "stream": False
    }

    # Make the API request
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def main():
    print("Welcome to Rio, a multilingual chatbot & teacher!")
    conversation_history = [
        {
            "role": "system",
            "content": "You're Rio, a multilingual chatbot that assesses the user's language and asks if your understanding is correct. Following which you speak in their initial language and give a fun fact regarding their chosen one and ask if the user would like to learn the language interactively with you. Please be a teacher from then onwards and encourage the user to ask pronunciations, spellings, etc."
        }
    ]
    
    while True:
        user_message = input("You: ")
        if user_message.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        
        # Append the user's message to the conversation history
        conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        response = generate_response(conversation_history)
        try:
            assistant_message = response['choices'][0]['message']['content']
            print(f"Rio: {assistant_message}")
            
            # Append the assistant's message to the conversation history
            conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
        except (KeyError, IndexError):
            print("Error: Unable to fetch response from Groq API.")
            print("Response:", response)

if __name__ == '__main__':
    main()
