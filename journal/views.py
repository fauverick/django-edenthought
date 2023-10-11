from django.shortcuts import render, redirect

from .forms import CreateUserForm, LoginForm, ThoughtForm, UpdateUserForm, UpdateProfileForm

from django.contrib.auth.models import auth

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .models import Thought, Profile

from django.contrib.auth.models import User

from django.core.mail import send_mail

from django.conf import settings

# Create your views here.

def homepage(request):
    return render(request, 'journal/index.html')

def register(request):

    form = CreateUserForm()

    if(request.method == 'POST'):
        form = CreateUserForm(request.POST)

        if form.is_valid():

            current_user = form.save(commit=False) #commit = false to stop the data from being posted

            form.save()

            #send welcoming email

            send_mail("Welcome to Eden Thought!", "Congratulation on creating your account", settings.DEFAULT_FROM_EMAIL, [current_user.email])

            profile = Profile.objects.create(user = current_user) #create new profile object with user field (the foreign key) set to current user

            messages.success(request, "User Created") #or messages.error(request, "") to afficher les erreurs

            return redirect("my_login")
    context = {'UserForm': form}

    return render(request, 'journal/register.html', context)

def my_login(request):

    form = LoginForm()

    if(request.method == 'POST'):
        form = LoginForm(request, data = request.POST)

        if form.is_valid:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password = password)

            if user is not None:
                auth.login(request, user)

                return redirect('dashboard')
    
    context = {'LoginForm': form}

    return render(request, 'journal/my_login.html', context)

def user_logout(request):
    auth.logout(request)
    return redirect("")

@login_required(login_url="my_login")
def dashboard(request):

    profile_pic = Profile.objects.get(user = request.user)

    context = {"ProfilePic": profile_pic}

    return render(request, 'journal/dashboard.html', context)

@login_required(login_url = "my_login")
def create_thought(request):

    form = ThoughtForm()

    if(request.method == 'POST'):
        form = ThoughtForm(request.POST)

        if form.is_valid():
            thought = form.save(commit=False) #save the form then wait to attach the user to the form (we have a user Foreign Key), otherwise its gonnabe posted to the databse
            thought.user = request.user #request.user is the user that's currently logged in
            thought.save()

            messages.success(request, f'Thought {thought.title} created')
            return redirect("my_thoughts")
    context = {"CreateThoughtForm": form}

    return render(request, 'journal/create_thought.html', context)

@login_required(login_url = "my_login")
def my_thoughts(request):

    current_user = request.user.id
    thought = Thought.objects.all().filter(user = current_user)

    context = {"AllThoughts": thought}

    return render(request, 'journal/my_thoughts.html', context)


@login_required(login_url = "my_login")
def update_thought(request, pk):

    try: 
        thought = Thought.objects.get(id = pk, user = request.user)
    except:
        return redirect("my_thoughts")

    form = ThoughtForm(instance = thought)

    if(request.method == 'POST'):
        form = ThoughtForm(request.POST, instance = thought)
        
        if form.is_valid():
            form.save()
            return redirect("my_thoughts")
    
    context = {"UpdateThought": form}

    return render(request, 'journal/update_thought.html', context)

@login_required(login_url = "my_login")
def delete_thought(request, pk):

    try:
        thought = Thought.objects.get(id = pk, user = request.user)
    except:
        return redirect("my_thoughts")
    
    if(request.method == 'POST'):
        thought.delete()
        return redirect("my_thoughts")
    
    context = {"DeleteThought": thought}

    return render(request, 'journal/delete_thought.html', context)

@login_required(login_url = "my_login")
def profile_management(request):

    form = UpdateUserForm(instance = request.user)

    profile = Profile.objects.get(user = request.user)

    form_pic = UpdateProfileForm(instance = profile)

    if (request.method == 'POST'):
        form = UpdateUserForm(request.POST, instance=request.user)

        form_pic = UpdateProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect("dashboard")
        
        if form_pic.is_valid():
            form_pic.save()
            return redirect("dashboard")
        
    context = {"UserUpdateForm": form, "ProfileUpdateForm": form_pic, "CurrentProfile": profile}

    return render(request, 'journal/profile_management.html', context)


@login_required(login_url = "my_login")
def delete_account(request):

    account = request.user

    if(request.method == 'POST'):
        deleteUser = User.objects.get(username = account)
        deleteUser.delete() 

        #account.delete() also works too, it's not in the course but i test and it works

        return redirect("")
    
    context = {"account": account}

    return render(request, 'journal/delete_account.html', context)