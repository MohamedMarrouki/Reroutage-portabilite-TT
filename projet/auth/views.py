from django.shortcuts import render, redirect
from django.contrib import auth
from django.core.validators import EMPTY_VALUES,RegexValidator,validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .helper import send_forget_mail 
import uuid

# Create your views here.


def loginn(request):
    error = False
    message = ""
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
                error = True
                message = "Wrong password"
                print("Wrong password")
        else:
            error = True
            message = "User does not exist"
            print("User does not exist")
    context = {
        'error':error,
        'message':message
    }
    return render(request, 'pages/login.html',context)


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
    user = auth.get_user(request)
    if user.is_authenticated:
        nom_utilisateur = user.username
        email_utilisateur = user.email
        nom = user.last_name + " " + user.first_name
        # prenom = user.first_name
    context = {'nom_utilisateur': nom_utilisateur,
               'email_utilisateur': email_utilisateur,
               'nom': nom
               }
    return render(request, 'pages/index.html', context)

def log_out(request):
    logout(request)
    return redirect('login')

def forget_password(request):
    error=False
    message=""
    try:
       if request.method=='POST':
           email= request.POST.get('email')
           
           if not User.objects.filter(email=email).first():
               error=True
               message = "User not found"
               context = {
                    'error':error,
                    'message':message
                }   
               return render(request, 'pages/forgot-password.html', context)
           
           user_obj=User.objects.get(email=email)
           token=str(uuid.uuid4)
           send_forget_mail(user_obj,token)

    except Exception as e:
        print(e)
        
        
    return render(request, 'pages/forgot-password.html')

def reset_password(request):
    return render(request, 'pages/reset-password.html')

def ma_vue(request):
    user = auth.get_user(request)
    if user.is_authenticated:
        nom_utilisateur = user.username
        context = {'nom_utilisateur': nom_utilisateur}
        return render(request, 'pages/index.html', context)


