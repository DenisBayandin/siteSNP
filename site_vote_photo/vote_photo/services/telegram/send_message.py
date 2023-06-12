import requests
from django.conf import settings


bot_token = settings.TELEGRAM_BOT_TOKEN


def send_message_is_telegram(user, message):
    if user.id_telegram is not None:
        requests.get(
            f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={user.id_telegram}&text='
            f'Вам пришло уведомление: {message}'
        )
