import requests
from django.http import HttpResponse
from rest_framework.views import APIView
from tbot import configs
from tbot.utils import get_bot

bot = get_bot()


class BotActivationView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            response = requests.get(
                f"{bot.base_url}/setWebhook?url={configs.BOT_WEBHOOK_URL}/bot/handler/")
            if response.status_code is not 200:
                # TODO handle specific errors
                return HttpResponse("There are some problems.")
            return HttpResponse("Activated")
        except Exception as e:
            return HttpResponse("There are some problems like this:  %s" % e)
