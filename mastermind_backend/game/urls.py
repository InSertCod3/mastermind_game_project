from django.urls import path

from . import views

urlpatterns = [
    path('ping', views.ping, name='ping'),
    path('create_game', views.create_game, name='create_game'),
    path('make_move', views.make_move, name='make_move'),
    path('leaderboards', views.leaderboards, name='leaderboards'),
]