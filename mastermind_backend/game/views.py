import uuid
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.template import loader
from game.models import Game
from game.tools import sequence_match


@api_view(['GET'])
def ping(request):
    """
    Ping the api for availability
    :::/api/ping

    Returns:
        dict -- {"status": "ok"},
    """
    return Response({"status": "ok"}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def create_game(request):
    """
    Creates a new game for user to play.
    :::/api/game/create_game?username=john_snow_2019
    
    Returns:
        dict -- {
                "status": "ok",
                "username": "Playone_Has_Entered",
                "game_id": "747f0b82-d0df-11e9-98c1-002522cf8548"
            }
    """
    r_username = request.GET['username']  # Url Arg ?username=XXXXXXX
    if not r_username:
        return Response({"status": "error", "message": "Error, Invalid Username."}, status=status.HTTP_400_BAD_REQUEST)
    G = Game(username=r_username)
    G.publish()
    return Response({"status": "ok", "username": G.username, "game_id": G.game_id}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def make_move(request):
    """
    Allow a player to make a move.
    :::/api/game/make_move?username=john_snow_2019&game_id=8af6477b6f6c492fb1723a6e4de3f3a3&variables=0,8,1,6

    Returns:
        dict -- {
                "status": "ok",
                "username": "Playone_Has_Entered",
                "game_id": "747f0b82-d0df-11e9-98c1-002522cf8548",
                "correct_variables": [],
                "retrys": 1,
                "game_complete": false
            }
    """
    r_username = request.GET['username']  # Url Arg ?username=XXXXXXX
    r_game_id = request.GET['game_id']  # Url Arg ?game_id=XXXXXXX
    r_variables = request.GET['variables']  # Url Arg ?game_id=XXXXXXX

    G = Game.objects.get(username=r_username, game_id=r_game_id)
    user_sequence = list(r_variables.split(","))
    if len(user_sequence) > 4:
        session_game_info = {"status": "sequence.too_many_variables", "message": "Received too many variables, limit is set to (4)."}
        return Response(session_game_info, status=status.HTTP_201_CREATED)
    game_correct_sequence = G.sequence.split(",")
    correct_variables = sequence_match(game_correct_sequence, user_sequence)  # Compare sets(...) & get matching numbers
    game_info = {"username": G.username, "retrys": G.retrys, "game_complete": G.game_complete, "game_id": G.game_id}
    if G.game_complete is True: # Check if our game completed already.
        session_game_info = {"status": "sequence.completed_already", "message": "Sequence was already solved."}
        return Response({**session_game_info, **game_info}, status=status.HTTP_201_CREATED)
    if G.retrys >= G.chance_limit: # Retry Limit Reached.
        session_game_info = {"status": "sequence.error.max_retrys", "message": "Max Retries Reached."}
        return Response({**session_game_info, **game_info}, status=status.HTTP_201_CREATED)
    if len(correct_variables) < len(game_correct_sequence):  # Incorrect Sequence.
        G.increments_retrys()  # Increment +1 to our tries.
        session_game_info = {"status": "sequence.error", "message": "Missing Variables.", "correct_variables": correct_variables}
        return Response({**session_game_info, **game_info}, status=status.HTTP_201_CREATED)
    else:
        G.mark_game_complete()  # Mark the game as completed
        session_game_info = {"status": "sequence.solved", "message": "Sequence Solved.", "correct_variables": correct_variables}
        return Response({**session_game_info, **game_info}, status=status.HTTP_201_CREATED)
    return Response({"status": "ok", "message": "Unexpected"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def leaderboards(request):
    """
    Leaderboard of users.
    :::/api/game/leaderboards
    
    Returns:
        dict -- {
                "status": "ok",
                "board": [
                    {
                        "username": "john_snow_2019",
                        "completed_games": 14,
                    }
                ]
            }
    """
    Games_Objects = Game.objects.all().filter(game_complete=True)
    board = {}
    for x in Games_Objects:
        if x.username not in board.keys():
            board[x.username] = {"completed_games": 0}
        board[x.username]["completed_games"] += 1
    return Response({"status": "ok", "board": board}, status=status.HTTP_201_CREATED)