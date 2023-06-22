from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/challenge/<str:challenge_id>", consumers.WordleConsumer.as_asgi()),
]