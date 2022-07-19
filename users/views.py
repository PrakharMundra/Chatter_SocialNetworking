from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm,FollowerForm
from .models import Profile
from django.views.generic import ListView
from django.core.mail import send_mail
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


def follower_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FollowerForm(request.POST,)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:\

            profiles = Profile.objects.all()
            new_follower = form.cleaned_data['username']
            
            for profile in profiles:
                if new_follower== profile.user.username:
                    request.user.profile.following.add(profile.user)
                    send_mail(
                           'Chatter',
                           'You got a new follower!!',
                           'f20212694@pilani.bits-pilani.ac.in',
                           [profile.user.email],
                           fail_silently=False
                            )
                    


    # if a GET (or any other method) we'll create a blank form
    else:
        form = FollowerForm()

    return render(request, 'users/follow.html', {'form': form})

class FollowerView(ListView):
    model = Profile
    template_name = 'users/followerlist.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'profiles'

class FollowersView(ListView):
    model = Profile
    template_name = 'users/followerslist.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'profiles'
