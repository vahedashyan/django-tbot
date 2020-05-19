from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import BaseBotAPIView
from .activation import BotActivationView

urlpatterns = [
    path('handler/', csrf_exempt(BaseBotAPIView.as_view()), name="handler"),
    path('activate/', BotActivationView.as_view(), name="activate"),
]
