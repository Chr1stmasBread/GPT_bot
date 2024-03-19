import requests
import telebot
from langdetect import detect  # Импортируем функцию для определения языка
from TOKEN import *

# Создание экземпляра бота
bot = telebot.TeleBot(TOKEN)

# Функция для отправки запроса к Yandex GPT
def generate_text(query, lang):
    # Определяем язык ответа на основе языка запроса
    if lang == 'ru':
        model_uri = f"gpt://{FOLDER_ID}/yandexgpt-lite"  # Русская модель
    else:
        model_uri = f"gpt://{FOLDER_ID}/yandexgpt-lite-en"  # Английская модель

    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        "modelUri": model_uri,
        "completionOptions": {
            "stream": False,
            "temperature": 0.8,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "user",
                "text": query
            }
        ]
    }

    response = requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
                             headers=headers,
                             json=data)

    if response.status_code == 200:
        text = response.json()["result"]["alternatives"][0]["message"]["text"]
        return text
    else:
        error_message = 'Invalid response received: code: {}, message: {}'.format(response.status_code, response.text)
        return error_message

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет! Для начала работы введите /generate для генерации истории.')

# Обработчик команды /generate
@bot.message_handler(commands=['generate'])
def generate(message):
    bot.reply_to(message, 'Введите запрос для генерации истории.')

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    query = message.text
    lang = detect(query)  # Определяем язык запроса
    generated_text = generate_text(query, lang)
    bot.reply_to(message, generated_text)

# Запуск бота
bot.polling()