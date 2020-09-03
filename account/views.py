from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages


# here we use Django built in authentication Loginview so this method is not in used
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], # here check the username which one is store in database and cd['username'] which one is came from login form
                                         password=cd['password']) # cd means clean data from form, username and password came from login form,if check these condition then 'user' is true
            if user is not None: # user is not none means the user is in database
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated '\
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


# login required checks whether the current user is authenticated,this login_required is mixin(django build in),without inherit from mixin any person enter into dashboard
@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # save the user object in database
            new_user.save()
            # create a user profile(user is the parameter of profile)
            Profile.objects.create(user=new_user) # here create a user profile object as a 'new_user', if i don't register then edit path will not work
            return render(request, 'account/register_done.html',
                                    {'new_user': new_user})
    else:
        user_form = UserRegistrationForm() # when using get method
    return render(request,'account/register.html',
                          {'user_form': user_form})

# for editing purpose,we ensure that the user is login or not,this works done by django automatically by usin mixin(login)
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated '\
                                      'successfully')
        else:
            messages.error(request, 'Error updating your profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})