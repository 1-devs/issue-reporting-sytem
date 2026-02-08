from django.shortcuts import redirect, render
from .Form import UserForm
from .models import User
from django.contrib.auth import authenticate, login as auth_login

def UserLogin(request):

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid Email or Password")    
    else:
        form = UserForm()
    return render(request, 'User_Aunthentication/Login.html', {'form': form})
