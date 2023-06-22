from django.contrib import admin
from .models import WordleChallenge, WordleAttempt, User

# Register your models here.
admin.site.register(WordleChallenge)
admin.site.register(WordleAttempt)
admin.site.register(User)