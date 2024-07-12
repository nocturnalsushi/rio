import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load your OpenAI API key from an environment variable
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Error: OpenAI API key not found. Please set it in the .env file.")
    exit()

openai.api_key = api_key

def translate_text(text, target_language):
    """
    Function to translate text to the target language using ChatGPT.
    Note: This is a simple translation function.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a translator. Translate the following text to {target_language}."},
                {"role": "user", "content": text}
            ]
        )
        translated_text = response['choices'][0]['message']['content'].strip()
        return translated_text
    except Exception as e:
        print(f"Error in translation: {e}")
        return "Translation error."

def chat_with_gpt3(user_input, language="en"):
    """
    Function to chat with GPT-3.5.
    """
    try:
        if language != "en":
            user_input = translate_text(user_input, "English")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        
        chatbot_response = response['choices'][0]['message']['content'].strip()

        if language != "en":
            chatbot_response = translate_text(chatbot_response, language)
        
        return chatbot_response
    except Exception as e:
        print(f"Error in chat: {e}")
        return "Chat error."

if __name__ == "__main__":
    print("Multilingual Chatbot is running...")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == "quit":
                break
            
            language = input("Language (e.g., en, es, fr): ").strip()
            if not language:
                language = "en"

            response = chat_with_gpt3(user_input, language)
            print(f"Bot: {response}")
        except KeyboardInterrupt:
            print("\nExiting the chatbot.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")