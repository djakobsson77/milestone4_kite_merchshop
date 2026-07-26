from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            template_name="pages/logged_out.html"
        ),
        name="logout",
    ),
    path("test/", views.test_page, name="test"),
    path("login/", views.test_page, name="login"),
    path("signup/", views.test_page, name="signup"),
    path("contact/", views.contact_dummy, name="contact"),
]
