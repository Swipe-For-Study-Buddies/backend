from django.conf.urls import url
from django.urls import path, include
from test_api.api import setProfile, getProfile, getSuggestionsAPI, approveSuggestionAPI, rejectSuggestionAPI


urlpatterns = [
    path('setUserProfile', setProfile.as_view(), name='set_profile'),
    path('getUserProfile', getProfile.as_view(), name='get_profile'),
    path('getSuggestions', getSuggestionsAPI.as_view(), name="suggestion"),
    path('approveSuggestion', approveSuggestionAPI.as_view(), name="suggestion"),
    path('rejectSuggestion', rejectSuggestionAPI.as_view(), name="suggestion"),
    
]