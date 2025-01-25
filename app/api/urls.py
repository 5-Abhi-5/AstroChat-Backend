from django.urls import path
from .views import google_login, refresh_access_token, save_user_zodiac, answer_prompt, index

urlpatterns = [
    path('', index, name='index'),
    path('google-login/', google_login, name='google_login'),
    path('refresh-access-token/', refresh_access_token, name='refresh_access_token'),
    path('user-zodiac/', save_user_zodiac, name='save_user_zodiac'),
    path('answer-prompt/', answer_prompt, name='answer_prompt')
]
