from django.urls import path
from .views import ProfileView, PasswordChangeView

urlpatterns = [
    path('settings/profile/', ProfileView.as_view(), name='profile'),
    path('settings/password-change/', PasswordChangeView.as_view(), name='password-change'),

]
