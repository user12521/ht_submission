from django.urls import path, include

from .views import *

urlpatterns = [
    path("septic/", SepticPresence.as_view()),
]
