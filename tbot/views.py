import json

from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView

from tbot.handler import BotUpdateHandler
from tbot.serializers import UpdateSerializer


class BaseBotAPIView(APIView):
    serializer_class = UpdateSerializer
    update_handler = BotUpdateHandler

    def get(self, request, *args, **kwargs):
        return HttpResponse("OK!")

    def post(self, request, *args, **kwargs):
        t_data = json.loads(request.body)
        serializer = self.serializer_class(data=t_data)
        serializer.is_valid(raise_exception=True)
        self.update_handler(serializer.validated_data)
        return JsonResponse({"ok": "POST request processed"})
