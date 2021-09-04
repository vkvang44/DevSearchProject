from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Profile


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
            print('Username does not exist')

        # authenticates user and checks if there exists a valid login
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # creates a session for the user in the database and its gonna add the session to the cookie so the website
            # knows if the user is logged in
            login(request, user)
            return redirect('profiles')
        else:
            print('Username OR Password is incorrect')

    return render(request, 'users/login_register.html', {})


def logoutUser(request):
    logout(request)
    return redirect('login')