from django.urls import path
from .views import homeView

app_name = 'images'

urlpatterns = [
    path('', homeView, name="index"),
]
