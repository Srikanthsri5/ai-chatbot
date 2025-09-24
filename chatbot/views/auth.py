from django.shortcuts import render, redirect
from django.contrib import auth
from .main import logger
from django.contrib.auth.models import User

def login(request):
    """Handle user login."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')


def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            error_message = "Passwords don't match"
            return render(request, 'register.html', {'error_message': error_message})

        try:
            user = User.objects.create_user(username, email, password1)
            user.save()
            auth.login(request, user)
            return redirect('chatbot')
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            error_message = "Error creating account. Username may already exist."
            return render(request, 'register.html', {'error_message': error_message})

    return render(request, 'register.html')


def logout(request):
    """Handle user logout."""
    auth.logout(request)
    return redirect('home')

