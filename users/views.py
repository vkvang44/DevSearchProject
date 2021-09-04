from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages
from .form import CustomUserCreationForm


# Create your views here.
def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profileObj = Profile.objects.get(id=pk)
    context = {'profile':profileObj}
    return render(request, 'users/user_profile.html', context)


def loginUser(request):
    page = 'login'

    # this statement makes sure the logged in user doesnt go back to the login page
    if request.user.is_authenticated:
        return redirect('profiles')
    #
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # simple try exception block to query the username from the database to see if they exist
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        # authenticates user and checks if there exists a valid login
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # creates a session for the user in the database and its gonna add the session to the cookie so the website
            # knows if the user is logged in
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username OR Password is incorrect')

    return render(request, 'users/login_register.html', {'page': page})


def logoutUser(request):
    logout(request)
    messages.error(request, 'Username was logged out!')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have created your profile!')
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'An error has occurred during registration')
    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)