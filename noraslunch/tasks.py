
from backend_test_lattus.celery import app
from backend_test_lattus.settings import SLACK_TOKEN, SLACK_CHANNEL
from noraslunch.models import Menu
import logging

logging.basicConfig(level=logging.DEBUG)

from slack import WebClient
from slack.errors import SlackApiError


@app.task()
def send_slack(menu_id):
    slack_token = SLACK_TOKEN
    client = WebClient(token=slack_token)

    menu = Menu.objects.get(id=menu_id)
    message= "Hola!\nDejo el menú de hoy :yum:\n\n"
    for index, meal in enumerate(menu.meal_set.all()):
        message += f"- :knife_fork_plate: Opción {index +1}: {meal.description}\n"
    message += f"\nClick <https://nora.cornershop.io/menu/{menu.id}|aquí> para elegir tu almuerzo."
    message += "\nTengan lindo día! :smile:"

    try:
        response = client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=message
        )
        menu.was_sent = True
        menu.save()
        resolution = True
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        resolution = False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'

    return resolution
