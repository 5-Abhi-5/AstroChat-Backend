from django.db import models
from django.contrib.auth.models import User



'''
Profile model that extends the User model to store additional information about the user.
Additional fields include an image URL and a Google ID.
'''
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.URLField(blank=True, null=True)
    google_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.email
    


'''
UserZodiac model that extends the User model to store the user's zodiac sign and date of birth.
'''
class UserZodiac(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    zodiac_sign = models.CharField(max_length=255)
    date_of_birth = models.CharField(max_length=255)
    
    def __str__(self):
        return self.zodiac_sign