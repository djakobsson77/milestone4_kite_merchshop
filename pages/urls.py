from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="pages/login.html"
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            template_name="pages/logged_out.html"
        ),
        name="logout",
    ),
    path("signup/", views.signup, name="signup"),
    path("contact/", views.contact, name="contact"),
    path("contact/success/", views.contact_success, name="contact_success"),
    path('checkout/', views.checkout, name='checkout'),
]
