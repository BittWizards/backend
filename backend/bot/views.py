import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Update

start_url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/"

button_reaction = {
    "report": "Эта ссылка вам в этом поможет!",
    "achiv": "Вот ваш список достижений!",
    "statistic": "Немного статистики",
    "profile": "Ваш профиль",
}


def get_keyboard() -> InlineKeyboardButton:
    keyboard = [
        [
            InlineKeyboardButton("Отправить отчет", callback_data="report"),
            InlineKeyboardButton("Достижения", callback_data="achiv"),
        ],
        [
            InlineKeyboardButton("Статистика", callback_data="statistic"),
            InlineKeyboardButton("Профиль", callback_data="profile"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


@api_view(["POST"])
def bot_view(request: Request) -> Response:
    data = request.data
    update = Update.de_json(data)
    if update.message:
        user_id = update.message.from_user.id
        keyboard = get_keyboard()
        url = start_url + "SendMessage"
        params = {
            "chat_id": user_id,
            "text": "Здравствуйте",
            "reply_markup": keyboard.to_dict(),
        }
        response = requests.post(url, json=params)
        print(response.json())
    elif update.callback_query:
        user_id = update.callback_query.from_user.id
        message_id = update.callback_query.message.message_id
        button = update.callback_query.data
        url = start_url + "editMessageText"
        params = {
            "chat_id": user_id,
            "message_id": message_id,
            "text": button_reaction[button],
        }
        response = requests.post(url, json=params)
        print(response.json())

    return Response({"detail": "ok"})
