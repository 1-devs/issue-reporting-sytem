from django.urls import path
from .views import ProfileView, PasswordChangeView, RegisterView, LeaderCreationView

urlpatterns = [
    path('settings/profile/', ProfileView.as_view(), name='profile'),
    path('settings/password-change/', PasswordChangeView.as_view(), name='password-change'),
    path('register/', RegisterView.as_view(), name='register'),
    path('create-leader/', LeaderCreationView.as_view(), name='create-leader'),

]