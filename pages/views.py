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
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        send_mail(
            "New Contact Form Message",
            f"From: {name}\nEmail: {email}\n\nMessage:\n{message}",
            settings.DEFAULT_FROM_EMAIL,
            ["djakobsson77@gmail.com"],
        )

        return redirect("contact_success")

    return redirect("home")


def contact_success(request):
    return render(request, "pages/contact_success.html")

def checkout(request):
    return render(request, 'store/checkout.html')
