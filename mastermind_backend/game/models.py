import uuid
import random
from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

def random_sequence(length=4, min_int=0, max_in=9) -> str:
    """
    Generates a random unique "," separated (str) sequence of numbers based a
    range of numbers provided.

    >>> random_sequence(length=4, min_int=0, max_in=9)
    >>> 8,5,2,4

    Keyword Arguments:
        length {int} -- Length limit of the sequence. (default: {4})
        min_int {int} -- Minimal integer in the number range. [description] (default: {0})
        max_in {int} -- Maximum integer in the number range.  [description] (default: {9})
    
    Returns:
        str -- Comma (",") Separated string. (EX. "1,2,3,4")
    """
    A = []
    while len(A) < length:
        r_int = random.randint(a=min_int, b=max_in)
        if str(r_int) not in A:
            A.append(str(r_int))
    return ",".join(A)


class Game(models.Model):
    username = models.TextField()
    game_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular game across whole library')
    sequence = models.CharField(default=random_sequence, max_length=20, help_text='The target sequence that the player must match.')
    chance_limit = models.IntegerField(default=10, help_text='The amount of chances the user has to guess the correct answer.')
    game_complete = models.BooleanField(default=False, help_text='If the player completed the game.')
    retrys = models.IntegerField(default=0, help_text='Current amount of tries the player attempted.')

    def increments_retrys(self):
        self.retrys += 1
        self.save()
    
    def mark_game_complete(self):
        self.game_complete = True
        self.save()

    def publish(self):
        self.save()

    def __str__(self):
        return str(self.game_id)
