from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import WordleChallenge, WordleAttempt, User
from .serializer import WordleChallengeSerializer, WordleAttemptSerializer

# Create your views here.


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/challenges/',
            'method': 'GET',
                        'body': None,
                        'description': 'Returns an array of challenges'
        },
        {
            'Endpoint': '/challenges/create',
            'method': 'POST',
                        'body': None,
                        'description': 'Creates a challenge'
        },
        {
            'Endpoint': '/challenges/challenge_id',
            'method': 'GET',
                        'body': None,
                        'description': 'Gets a challenge by challenge_id.'
        },
    ]
    return Response(routes)


@api_view(['GET'])
def getChallengeByID(request, challenge_id):
    challenge = WordleChallenge.objects.get(challenge_id=challenge_id)
    serializer = WordleChallengeSerializer(challenge, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def createChallenge(request, user_id):

    word = request.data['word']
    if len(word) != 5 or not word.islower():
        return Response({'error': 'Invalid word. The word must be 5 letters long and consist of lowercase letters.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    challenge = WordleChallenge.objects.create(
        creator=user,
        word=word
    )
    serializer = WordleChallengeSerializer(challenge, many=False)

    return Response(serializer.data)

@api_view(['POST'])
def makeGuess(request):
    newGuess = request.data['guess']
    challenge_id = request.data['challengeID']
    user_id = request.data['userID']

    if len(newGuess) != 5 or not newGuess.islower():
        return Response({'error': 'Invalid word. The word must be 5 letters long and consist of lowercase letters.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        challenge = WordleChallenge.objects.get(challenge_id=challenge_id)
    except WordleChallenge.DoesNotExist:
        return Response({'error': 'Challenge not found.'}, status=status.HTTP_404_NOT_FOUND)

    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    try:
        existingAttempt = WordleAttempt.objects.get(challenge=challenge, user=user)

        if (challenge.word in existingAttempt.guesses):
            return Response({ 'error': 'Correct word has already been guessed.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(existingAttempt.guesses) >= 6:
            return Response({'error': 'Maximum number of guesses (6) already reached.'}, status=status.HTTP_400_BAD_REQUEST)

        existingAttempt.guesses.append(newGuess)
        existingAttempt.save()
        serializer = WordleAttemptSerializer(existingAttempt, many=False)
        return Response(serializer.data)

    except WordleAttempt.DoesNotExist:
        attempt = WordleAttempt.objects.create(
            challenge=challenge,
            guesses=[newGuess],
            user=user
        )
        serializer = WordleAttemptSerializer(attempt, many=False)
        return Response(serializer.data)

@api_view(['GET'])
def getGuesses(request, challenge_id, user_id):
    try:
        challenge = WordleChallenge.objects.get(challenge_id=challenge_id)
    except WordleChallenge.DoesNotExist:
        return Response({'error': 'Challenge not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        attempt = WordleAttempt.objects.get(challenge=challenge, user_id=user_id)
        serializer = WordleAttemptSerializer(attempt, many=False)
        return Response(serializer.data)
    except WordleAttempt.DoesNotExist:
        return Response({'error': 'Attempt not found.'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def getAllAttempts(request, challenge_id, user_id):
    try:
        challenge = WordleChallenge.objects.get(challenge_id=challenge_id)
    except WordleChallenge.DoesNotExist:
        return Response({'error': 'Challenge not found.'}, status=status.HTTP_404_NOT_FOUND)

    attempts = WordleAttempt.objects.filter(challenge=challenge).exclude(user__user_id=user_id)
    serializer = WordleAttemptSerializer(attempts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getAllUsersForChallenge(request, challenge_id, user_id):
    try:
        challenge = WordleChallenge.objects.get(challenge_id=challenge_id)
    except WordleChallenge.DoesNotExist:
        return Response({'error': 'Challenge not found.'}, status=status.HTTP_404_NOT_FOUND)

    attempts = WordleAttempt.objects.filter(challenge=challenge)
    users = [attempt.user for attempt in attempts if attempt.user.user_id != user_id]

    return Response(users)

@api_view(['POST'])
def createUser(request):
    user_id = request.data.get('user_id')
    nickname = request.data.get('nickname')

    if nickname is None or user_id is None:
        return Response({'error': 'user_id and nickname are required.'}, status=status.HTTP_400_BAD_REQUEST)

    print(user_id)
    User.objects.create(user_id=user_id, nickname=nickname)
    return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def updateUser(request, user_id):
    nickname = request.data.get('nickname')

    if nickname is None:
        return Response({'error': 'Nickname is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    user.nickname = nickname
    user.save()
    return Response({'message': 'User updated successfully'})

@api_view(['GET'])
def getRecentChallenges(request, num_challenges):
    num_challenges = int(num_challenges)
    if num_challenges < 0 or num_challenges >= 25:
        return Response({'error': 'Number of challenges should be a positive number less than 25.'}, status=status.HTTP_400_BAD_REQUEST)
    
    user_id = request.query_params.get('user_id')
    if user_id is None:
        return Response({'error': 'Must pass in a user id.'}, status=status.HTTP_400_BAD_REQUEST)
    
    challenges = WordleChallenge.objects.order_by('-created_at')[num_challenges:num_challenges+5]
    serializer = WordleChallengeSerializer(challenges, many=True)
    
    challenge_data = serializer.data
    
    for data in challenge_data:
        challenge_id = data['challenge_id']
        attempts = WordleAttempt.objects.filter(challenge_id=challenge_id)
        data['num_attempts'] = attempts.count()

        user_attempt = attempts.filter(user_id=user_id).first()
        
        if not user_attempt:
            data['completed_status'] = 'noattempt'
        else:
            # if user_attempt guesses contains the correct word then data['completed_status'] = 'won'
            # else if user_attempt guesses is less than length 6 then data['completed_status'] = 'inprogress'
            # else data['completed_status'] = 'lost'
            # Check if user_attempt guesses is 6
            guesses = user_attempt.guesses if user_attempt.guesses else []
            correct_word = data['word']
            
            if correct_word in guesses:
                data['completed_status'] = 'won'
                data['num_guesses'] = len(guesses)
            elif len(guesses) < 6:
                data['completed_status'] = 'inprogress'
                data['num_guesses'] = len(guesses)
            else:
                data['completed_status'] = 'lost'

        creator_id = data['creator']
        creator = User.objects.get(user_id=creator_id)
        data['creator'] = creator.nickname
    
    return Response(challenge_data)