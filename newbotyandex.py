import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Функция для взаимодействия с YandexGPT
def ask_yandex_gpt(question):
    headers = {
        'Authorization': 'Bearer AQVN1c3Eyb0X9lc0ssVdL5yucp6moG-XxbWfRpk1',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "gpt-3.5-turbo",  # Замените на нужную модель
        "messages": [{"role": "user", "content": question}]
    }

    response = requests.post('https://api.yandex.com/gpt', headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "Упс, кажется бот спит."

# Функция для старта
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Спросить YandexGPT", callback_data='ask_gpt')],
        [InlineKeyboardButton("Помощь", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Я бот. Выберите опцию:', reply_markup=reply_markup)

# Функция для обработки кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'ask_gpt':
        await query.edit_message_text(text="Напишите свой вопрос:")
        return

    if query.data == 'help':
        await query.edit_message_text(text="Я могу отвечать на ваши вопросы с помощью YandexGPT!")

# Функция для обработки текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_question = update.message.text
    answer = ask_yandex_gpt(user_question)
    await update.message.reply_text(answer)

if __name__ == '__main__':
    application = ApplicationBuilder().token("7869555754:AAFlPNauYT35gvXBgplqQuMaFSnpwK0kZiM").build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

