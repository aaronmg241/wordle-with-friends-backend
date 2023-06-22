from django.db import models
import uuid
class User(models.Model):
	user_id = models.UUIDField(default=uuid.uuid4, editable=True, primary_key=True)
	nickname = models.CharField(max_length=20)

	def __str__(self):
		return f"{self.nickname} - {self.user_id}"
	
class WordleChallenge(models.Model):
	challenge_id = models.CharField(max_length=10, unique=True, editable=False, primary_key=True)
	creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenges')
	word = models.CharField(max_length=20)  # The actual word to be guessed
	created_at = models.DateTimeField(auto_now_add=True)
    
	def save(self, *args, **kwargs):
		if not self.challenge_id:
			self.challenge_id = str(uuid.uuid4().hex[:10])
		super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.word} - Wordle Challenge by {self.creator} - {self.challenge_id}"

	
class WordleAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts', null=True)
    challenge = models.ForeignKey(WordleChallenge, on_delete=models.CASCADE, related_name='attempts')
    guesses = models.JSONField()  # Array field to store the guesses
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Attempt for Challenge: {self.challenge} by {self.user}"

