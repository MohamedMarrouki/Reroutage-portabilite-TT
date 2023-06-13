from django.shortcuts import render, redirect
from django.core.validators import EMPTY_VALUES,RegexValidator,validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def loginn(request):
    # return render(request, 'pages/login.html')
    if request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        user = User.objects.filter(email=email).first()
        if user:
            auth_user = authenticate(username=user.username, password=password)
            if auth_user:
                login(request, auth_user)
                return redirect('home1')
            else:
                print("mot de pass incorrecte")
        else:
            print("User does not exist")
        
    return render(request, 'pages/login.html')


def register(request):
    error = False
    message = ""
    if request.method == "POST":
        Fname = request.POST.get('first_name', None)
        Lname = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        passwd = request.POST.get('password', None)
        r_passwd = request.POST.get('re_password', None)
        try:
            validate_email(email)
        except:
            error = True
            message = "Email invalide"
        if error == False:    
            if passwd != r_passwd:
                error = True
                message = "Mot de passe non conforme"
        user = User.objects.filter(email=email).first()
        if user:
            error = True
            message = f"Un utilisateur avec email {email} existe déjà !"

        if error == False:
            user = User(
                username = email,
                email = email,
                first_name = Fname,
                last_name = Lname,
            )
            user.save()

            user.password = passwd
            user.set_password(user.password)
            user.save()

            return redirect('login')


    context = {
        'error':error,
        'message':message
    }   
    return render(request, 'pages/register.html', context)

@login_required(login_url='login')
def home(request):
   return render(request, 'pages/index.html')

def log_out(request):
    logout(request)
    return redirect('login')
