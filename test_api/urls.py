from django.conf.urls import url
from django.urls import path, include
from .api import RegisterApi, ActivateAPI

urlpatterns = [
      path('register', RegisterApi.as_view()),
      path('activateAccount', ActivateAPI.as_view()),
]