# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    # The following paths are commented out but can be enabled as needed.
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.profile, name='profile'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('admin-only/', views.admin_only_view, name='admin_only'),
]
