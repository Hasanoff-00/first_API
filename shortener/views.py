from django.shortcuts import render, redirect, get_object_or_404
from .models import URL
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *

@login_required
def home(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        url, created = URL.objects.get_or_create(original_url=original_url, owner=request.user)
        return render(request, 'home.html', {'url': url})
    return render(request, 'home.html')


def redirect_url(request, short_code):
    url = get_object_or_404(URL, short_code=short_code)
    return redirect(url.original_url)


def signup(request):
    if request.method == 'POST':
        form = SignUp(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shortener:login')
    else:
        form = SignUp()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('shortener:home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('shortener:login')