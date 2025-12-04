import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY не найден в .env файле")

genai.configure(api_key=api_key)

def get_chat_response(user_message):
    try:
        # Используем модель из вашего списка
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        return f"Ошибка при обращении к Gemini: {str(e)}"

if __name__ == "__main__":
    print(get_chat_response("Привет!"))