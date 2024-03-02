import os

import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from telebot.types import (
    File,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    User,
    UserProfilePhotos,
    WebAppInfo,
)

from ambassadors.models import Ambassador

start_url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/"
download_file_url = f"https://api.telegram.org/file/bot{settings.BOT_TOKEN}/"


def get_keyboard() -> InlineKeyboardMarkup:
    webapp_info = WebAppInfo(f"https://{settings.DOMAIN}/")
    url = "https://forms.yandex.ru/u/65dd3da6eb61461c0f8e3229/"
    keyboard = [
        [
            InlineKeyboardButton("Отправить отчет", url=url),
        ],
        [
            InlineKeyboardButton(
                "Ваша страница",
                web_app=webapp_info,
            ),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_new_ambassador_keyboard() -> InlineKeyboardMarkup:
    url = "https://forms.yandex.ru/u/65d7978e90fa7b9905614294/"
    keyboard = [
        [
            InlineKeyboardButton("Анкета амбассадора", url=url),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_image_if_not_exists(ambassador: Ambassador, user: User) -> None:
    if ambassador.tg_id is None:
        url = start_url + "getUserProfilePhotos"
        params = {
            "user_id": user.id,
            "limit": 1,
        }
        response = requests.post(url, json=params)
        user_photos = UserProfilePhotos.de_json(response.json()["result"])
        if user_photos.photos:
            photo = (
                user_photos.photos[0][1]
                if len(user_photos.photos[0]) > 0
                else user_photos.photos[0][0]
            )
        else:
            ambassador.tg_id = user.id
            ambassador.save()
            return
        url = start_url + "getFile"
        params = {
            "file_id": photo.file_id,
        }
        response = requests.post(url, json=params)
        file = File.de_json(response.json()["result"])
        file_path = os.path.join(
            settings.MEDIA_ROOT, "profiles", f"{user.username}.jpg"
        )
        response = requests.get(download_file_url + file.file_path)
        with open(file_path, "wb") as f:
            f.write(response.content)
        ambassador.tg_id = user.id
        ambassador.image = f"profiles/{user.username}.jpg"
        ambassador.save()


@api_view(["POST"])
def bot_view(request: Request) -> Response:
    data = request.data
    update = Update.de_json(data)
    if update.message:
        try:
            user = update.message.from_user
        except Exception:
            return Response({"detail": "ok"})
        url = start_url + "SendMessage"
        try:
            ambassador = Ambassador.objects.get(tg_acc=user.username)
        except Exception:
            keyboard = get_new_ambassador_keyboard()
            params = {
                "chat_id": user.id,
                "text": "Кажется, мы еще не знакомы, заполни пожалуйста эту анкету:",
                "reply_markup": keyboard.to_dict(),
            }
            requests.post(url, json=params)
            return Response({"detail": "ok"})
        get_image_if_not_exists(ambassador, user)
        keyboard = get_keyboard()
        params = {
            "chat_id": user.id,
            "text": f"Привет, {ambassador.first_name}!",
            "reply_markup": keyboard.to_dict(),
        }
        requests.post(url, json=params)
    # elif update.callback_query:
    #     user_id = update.callback_query.from_user.id
    #     message_id = update.callback_query.message.message_id
    #     button = update.callback_query.data
    #     url = start_url + "editMessageText"
    #     params = {
    #         "chat_id": user_id,
    #         "message_id": message_id,
    #         "text": button_reaction[button],
    #     }
    #     requests.post(url, json=params)
    return Response({"detail": "ok"})