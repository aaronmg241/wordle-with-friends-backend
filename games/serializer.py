from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import WordleChallenge, WordleAttempt, User

class WordleChallengeSerializer(ModelSerializer):
    class Meta:
        model = WordleChallenge
        fields = '__all__'

class WordleAttemptSerializer(ModelSerializer):

    user = SerializerMethodField()

    def get_user(self, obj):
        user = {
            'user_id': obj.user.nickname + str(obj.user.user_id)[:10],
            'nickname': obj.user.nickname
        }
        return user
    
    class Meta:
        model = WordleAttempt
        fields = '__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
