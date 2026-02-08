from django.urls import path, include
from .views import LogoutView 

urlpatterns = [

    path('logout/', LogoutView.as_view(), name='auth_logout'),

    # 2. Password Reset Endpoints
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]