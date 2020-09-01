from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from User.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            age = form.cleaned_data.get('age')
            weight = form.cleaned_data.get('weight')
            height = form.cleaned_data.get('height')
            gender = form.cleaned_data.get('gender')
            user = authenticate(username=username, password=raw_password, email=email,
             age=age, weight=weight, height=height, gender=gender)
            login(request, user)
            return redirect('FoodInfo:service')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def update_user(request):
    if request.method == 'POST':
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        if user_change_form.is_valid():
            user_change_form.save()
            return redirect('FoodInfo:mypage')

    else:
        user_change_form = CustomUserChangeForm(instance=request.user)
    return render(request, 'update.html', {'user_change_form': user_change_form})