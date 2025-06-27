# users/urls.py
from django.urls import path
from .views import SignupView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    # You would add profile, logout, etc. views here
]
