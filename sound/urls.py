
from django.urls import path, include
from .views import (SoundList, SoundDetails, 
                    SoundUpdate, SoundDelete, SoundCreate , 
                    Hello , updateplay , updatelike , AlbumList , mostplayedsong)

urlpatterns = [
    path('list/',  SoundList.as_view()),
    path('list/<int:pk>/', SoundDetails.as_view()),
    path('list/update/<int:pk>', SoundUpdate.as_view()),
    path('list/delete/<int:pk>', SoundDelete.as_view()),
    path('create/', SoundCreate.as_view()),
    path('hello/',Hello.as_view()),
    path('played/<int:pk>' , updateplay),
    path('like/<int:pk>' , updatelike),
    path('album/<category>/' , AlbumList.as_view()),
    path('mostplayed/' , mostplayedsong),
]
