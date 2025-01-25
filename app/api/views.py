import os
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from .models import Profile, UserZodiac
from .utils import generate_openai_response, generate_prompt



google_client_id = os.getenv('GOOGLE_CLIENT_ID')



def index(request):
    return HttpResponse("Hey, You've reached AstroChat Backend!")



'''
Google login endpoint that receives a token from the frontend and verifies it with Google's API.
If the token is valid, the user is created or updated in the database and a response with an access token and refresh token is returned.
'''
@api_view(['POST'])
def google_login(request):
    token = request.data.get('token')
    print(token)
    
    if not token:
        return Response({'error': 'Token not provided'}, status=400)

    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request(), google_client_id)

        email = id_info.get('email')
        first_name = id_info.get('given_name', '')
        last_name = id_info.get('family_name', '')
        google_id = id_info.get('sub')  
        profile_picture = id_info.get('picture', '')

        if not email:
            raise ValidationError("Google token is invalid. No email found.")
        
        '''Test this (Error of object not Iterable)'''
        user, created = User.objects.get_or_create(
            username=email,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
            },
        )

        if created:
            Profile.objects.create(user=user, google_id=google_id, profile_picture=profile_picture)
            
        else:
            profile = user.profile
            profile.google_id = google_id
            profile.profile_picture = profile_picture
            profile.save()
            
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)
        
        return Response({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'email': user.email,
                'name': f"{user.first_name} {user.last_name}",
                'profile_picture': profile_picture,
            }
        })
        
    except ValueError as e:
        return Response({'error': 'Invalid token', 'details': str(e)}, status=400)



'''
Accepts a refresh token and returns a new access token.
'''
@api_view(['POST'])
def refresh_access_token(request):
    refresh_token = request.data.get('refresh_token')

    if not refresh_token:
        return Response({'error': 'Refresh token is required'}, status=400)

    try:
        refresh = RefreshToken(refresh_token)
        refesh_token = str(refresh)
        access_token = str(refresh.access_token)

        return Response({
            'access-token': access_token,
            'refresh-token': refresh_token
        }, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=400)



'''
Get the zodiac sign and date of birth of the user and store it in the database.
Authentication is required.
'''
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_user_zodiac(request):
    user = request.user
    zodiac_sign = request.data.get('zodiac_sign')
    date_of_birth = request.data.get('date_of_birth')
    
    print(zodiac_sign)
    print(date_of_birth)
    
    if not date_of_birth or not zodiac_sign:
        return Response({'error': 'Data insufficient'}, status=400)
    
    try:
        '''Test this (Error of object not Iterable)'''
        user_zodiac, created= UserZodiac.objects.get_or_create(user)
        user_zodiac.date_of_birth = date_of_birth
        user_zodiac.zodiac_sign = zodiac_sign
        user_zodiac.save()

        return Response({
            'message': 'Profile updated successfully',
            'date_of_birth': str(user_zodiac.date_of_birth),
            'zodiac_sign': user_zodiac.zodiac_sign,
        }, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=400)



'''
Generate a response to a user prompt from OpenAI API and return it to the frontend.
Authentication is required.
'''
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def answer_prompt(request):
    user_prompt = request.data.get("prompt")
    print(user_prompt)
    
    if not user_prompt:
        return Response({"error": "No prompt provided"}, status=400)
    
    prompt= generate_prompt(user_prompt)
    print(prompt)
    
    try:
        response = generate_openai_response(prompt)
        print(response)
        return Response({"response": response})
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)



