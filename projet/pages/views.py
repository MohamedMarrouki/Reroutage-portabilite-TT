from django.shortcuts import render

# Create your views here.
def home(request):
   return render(request, 'pages/login.html')
   #return HttpResponse('bonjour')