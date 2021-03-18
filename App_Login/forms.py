from django.forms import ModelForm
from .models import User, Profile

from django.contrib.auth.forms import UserCreationForm

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',) #eita automatically hobe..amra user ke shuvida dibo na set korar

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
