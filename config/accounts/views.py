from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)        #hazır login fonksiyonu
            return redirect("home")
    
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {"form" : form})



def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)    #hazır login fonksiyonu
            return redirect('home')
    else:
        form = AuthenticationForm(request)

    return render(request, 'accounts/login.html', {"form" : form})



def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def get_account(request):
    return render(request, 'accounts/account.html')