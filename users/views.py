from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Profile, Message
from django.contrib import messages
from .form import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm, ExperienceForm
from django.contrib.auth.decorators import login_required
from .utils import searchProfiles, profilePagination


# Create your views here.
def profiles(request):
    profiles, search_query = searchProfiles(request)
    paginator, profiles, custom_range = profilePagination(request, profiles)
    context = {'profiles': profiles, 'search_query': search_query, 'paginator':paginator, 'custom_range':custom_range}
    return render(request, 'users/profiles.html', context)


"""
IMPORTANT: Because I separated the profiles and user model, I have to use signals to update the user model itself
when I make updates to the profile model on the website. Look at updateProfile() in signals.py to understand how 
to set it up
"""
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
        # .lower() makes sure that username is lower cased to avoid case sensitivity
        username = request.POST['username'].lower()
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
            # the if method allows for a get request to be processed (see project.html line 61 for !next path)
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
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

        else:
            messages.error(request, 'An error has occurred during registration')


    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


@login_required(login_url='login')
def userAccount(request):
    # get the logged in user by using request.user.profile
    profile = request.user.profile
    context = {'profile':profile, }
    return render(request, 'users/account.html', context)



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



# uuid issues when connecting with postgre database
@login_required(login_url='login')
def createExperience(request):
    profile = request.user.profile
    form = ExperienceForm()

    if request.method == "POST":
        form = ExperienceForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.owner = profile
            exp.save()
            messages.success(request, 'Experience was added!')
            return redirect('account')

    context = {'form':form}
    return render(request, 'users/experience_form.html', context)

@login_required(login_url='login')
def updateExperience(request, pk):
    profile = request.user.profile
    exp = profile.experience_set.get(id=pk)
    form = ExperienceForm(instance=exp)

    if request.method == "POST":
        form = ExperienceForm(request.POST, instance=exp)
        if form.is_valid():
            exp.save()
            messages.success(request, 'Experience was updated!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/experience_form.html', context)


@login_required(login_url='login')
def deleteExp(request, pk):
    profile = request.user.profile
    exp = profile.experience_set.get(id=pk)
    if request.method == "POST":
        exp.delete()
        messages.success(request, 'Experience was deleted!')
        return redirect('account')
    context = {'object': exp}
    return render(request, 'delete_obj.html', context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added!')
            return redirect('account')

    context = {'form':form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            skill.save()
            messages.success(request, 'Skill was updated!')
            return redirect('account')

    context = {'form':form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request, 'Skill was deleted!')
        return redirect('account')
    context = {'object': skill}
    return render(request, 'delete_obj.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
   # unreadCount = messageRequests.filter(is_read=False).count()
    context={'messageRequests':messageRequests}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def messagePage(request, pk):
    message = Message.objects.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def sendMessage(request, pk):
    form = MessageForm()
    receiver = Profile.objects.get(id=pk)
    try:
        sender=request.user.profile
    except:
        sender = None;
    if request.method=="POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = receiver
            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()
            messages.success(request, 'Your message was successfully sent!')
            return redirect('user_profile', pk=receiver.id)
    context={'form': form, 'receiver':receiver}
    return render(request, 'users/message_form.html', context)