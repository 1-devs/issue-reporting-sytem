from django.urls import path
<<<<<<< HEAD
from .views import ProfileView, PasswordChangeView

urlpatterns = [
    path('settings/profile/', ProfileView.as_view(), name='profile'),
    path('settings/password-change/', PasswordChangeView.as_view(), name='password-change'),

]
=======
from .views import RegisterView


urlpatterns = [    
    path('register/', RegisterView.as_view(), name='register'),
    
]
>>>>>>> ac6aa502f4f39c1f251942db163918b4a6f36af6
