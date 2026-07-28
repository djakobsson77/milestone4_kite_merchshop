from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path("<int:pk>/", views.product_detail, name="product_detail"),
]
