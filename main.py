import requests
import telebot
from TOKEN import *

# Создание экземпляра бота
bot = telebot.TeleBot(TOKEN)

# Функция для отправки запроса к Yandex GPT
def generate_text(genre, hero, universe):
    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Content-Type': 'application/json'
    }
    data = {
        "modelUri": f"gpt://{folder_id}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "user",
                "text": f"Generate story with genre: {genre}, hero: {hero}, universe: {universe}"
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
    genre = 'Fantasy'  # Пример значения параметра
    hero = 'Knight'     # Пример значения параметра
    universe = 'Middle Earth'  # Пример значения параметра
    text = generate_text(genre, hero, universe)
    bot.reply_to(message, text)

# Обработчик всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Запуск бота
bot.polling()