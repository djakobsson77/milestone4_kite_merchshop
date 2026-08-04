from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def home(request):
    return render(request, 'pages/home.html')

def about(request):
    return render(request, 'pages/about.html')

def gallery(request):
    return render(request, 'pages/gallery.html')

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "pages/signup.html", {"form": form})

def contact(request):
    return render(request, "pages/contact.html")

    return redirect("contact_success")

    return redirect("home")


def contact_success(request):
    return render(request, "pages/contact_success.html")