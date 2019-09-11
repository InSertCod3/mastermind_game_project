import uuid
import random
from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

def random_sequence(length=4, min_int=0, max_in=9):
    A = []
    while len(A) < length:
        r_int = random.randint(a=min_int, b=max_in)
        if str(r_int) not in A:
            A.append(str(r_int))
    return ",".join(A)


class Game(models.Model):
    username = models.TextField()
    game_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    sequence = models.CharField(default=random_sequence, max_length=20)
    chance_limit = models.IntegerField(default=10)
    game_complete = models.BooleanField(default=False)
    retrys = models.IntegerField(default=0)

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
