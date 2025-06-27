
from rest_framework import generics, permissions
from .serializers import UserRegistrationSerializer
# Create your views here.
# users/views.py

class SignupView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny] # Anyone can sign up
