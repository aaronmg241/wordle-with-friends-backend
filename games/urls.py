from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes, name='routes'),
    path('challenges/create/<str:user_id>', views.createChallenge, name='create-challenge'),
    path('challenges/<str:challenge_id>', views.getChallengeByID, name='get-challenge'),
    path('challenges/getUsers/<str:challenge_id>/<str:user_id>', views.getAllUsersForChallenge, name='get-relevent-users'),
    path('attempts/create', views.makeGuess, name='make-guess'),
    path('attempts/<str:challenge_id>/<str:user_id>', views.getGuesses, name='get-guesses'),
    path('other-attempts/<str:challenge_id>/<str:user_id>', views.getAllAttempts, name='get-other-attempts'),
    path('user/create', view=views.createUser),
    path('user/update/<str:user_id>', view=views.updateUser)
]