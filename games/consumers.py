import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import WordleAttempt, WordleChallenge, User
from .serializer import WordleAttemptSerializer


class WordleConsumer(WebsocketConsumer):
    def connect(self):
        self.challenge_id = self.scope['url_route']['kwargs']['challenge_id']
        self.room_group_name = 'challenge_%s' % self.challenge_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        challengeID = text_data_json["challengeID"]
        userID = text_data_json["userID"]
        newGuess = text_data_json["guess"]

        # Validate the guess
        if len(newGuess) != 5 or not newGuess.islower():
            # Handle invalid guess (e.g., send an error message back to the client)
            return

        try:
            challenge = WordleChallenge.objects.get(challenge_id=challengeID)
        except WordleChallenge.DoesNotExist:
            # Handle challenge not found (e.g., send an error message back to the client)
            return

        try:
            user = User.objects.get(user_id=userID)
            attempt = WordleAttempt.objects.get(challenge=challenge, user=user)
            if challenge.word in attempt.guesses:
                # Handle correct word already guessed (e.g., send an error message back to the client)
                return

            if len(attempt.guesses) >= 6:
                # Handle maximum number of guesses reached (e.g., send an error message back to the client)
                return

            attempt.guesses.append(newGuess)
            attempt.save()

        except WordleAttempt.DoesNotExist:
            attempt = WordleAttempt.objects.create(
                challenge=challenge,
                guesses=[newGuess],
                user_id=userID
            )

        # Broadcast the updated guess to the room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'new_guess',
                'guesses': attempt.guesses,
                'nickname': attempt.user.nickname,
                'filteredUserID': str(attempt.user.user_id)[:10]
            }
        )

    # Receive guess update from room group
    def new_guess(self, event):

        # Send the guess update to the WebSocket
        self.send(text_data=json.dumps({
            'guesses': event['guesses'],
            'user_id': event['nickname'] + event['filteredUserID'],
            'nickname': event['nickname']
        }))