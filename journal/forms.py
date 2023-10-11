from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput

from django.forms import ModelForm

from .models import Thought, Profile

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2'] #the User model is from django's built in library

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

class ThoughtForm(ModelForm):  #use ModelForm for custom form (forms that're not in django's built in library)
    class Meta:
        model = Thought
        # fields = '__all__' #to use all fields list in Thought model in models.py
        fields = ['title', 'content',] #user field should be  attached to the thought form using the current user info instead of using user's input
        # exclude = ['user',] # another way to exclude the user field 

class UpdateUserForm(ModelForm): 

    password = None

    class Meta:
        model = User
        fields = ['username', 'email',] #the User model is from django's built in library, we dont update password here
        exclude = ['password1', 'password2',]    

class UpdateProfileForm(ModelForm):

    profile_pic = forms.ImageField(widget = forms.FileInput(attrs = {'class': 'form-control-file'}))

    class Meta:
        model = Profile
        fields = ['profile_pic',]
