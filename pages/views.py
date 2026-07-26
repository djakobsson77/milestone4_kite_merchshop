from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'pages/home.html')

def about(request):
    return render(request, 'pages/about.html')

def gallery(request):
    return render(request, 'pages/gallery.html')

def test_page(request):
    return render(request, "pages/test.html")

def contact_dummy(request):
    if request.method == "POST":
        # Ignorera POST helt – bara returnera något
        return render(request, "pages/test.html")
    return render(request, "pages/test.html")
