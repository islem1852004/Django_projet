# UserApp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegisterFrom
from django.contrib.auth import logout

def register(request):
    if request.method == "POST":
        form = UserRegisterFrom(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie !")
            return redirect("login")  # ou "home"
    else:
        form = UserRegisterFrom()

    return render(request, "register.html", {"form": form})
def logout_view(req):
    logout(req)
    return redirect("login")
