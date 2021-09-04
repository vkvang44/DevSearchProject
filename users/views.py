from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages
from .form import CustomUserCreationForm, ProfileForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}

    """ 
    different method to query the skill fields depending on the skills having description or not
    topSkills = profile.skill_set.exclude(description_exact="")
    otherSkills = profile.skill_set.filter(description="")
    """

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
            login(request, user)
            return redirect('edit_account')
        '''
        else:
            messages.error(request, 'An error has occurred during registration')
        '''

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


@login_required(login_url='login')
def userAccount(request):
    # get the logged in user by using request.user.profile
    profile = request.user.profile
    context = {'profile':profile, }
    return render(request, 'users/account.html', context)


"""
IMPORTANT: Because I separated the profiles and user model, I have to use signals to update the user model itself
when I make updates to the profile model on the website. Look at updateProfile() in signals.py to understand how 
to set it up
"""
@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form':form}
    return render(request, 'users/profile_form.html', context)