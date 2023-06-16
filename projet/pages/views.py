from django.shortcuts import render,redirect
from . models import *
from django.conf import settings as ss
from django.db import OperationalError


# Create your views here.
# def home(request):
#    return render(request, 'pages/login.html')
   #return HttpResponse('bonjour')
   
nomfich=''

def home(request):
    context = {
        "data":myuploadfile.objects.all(),
    }
    return render(request,"pages/upload_file_final.html",context)
   # return render(request,"pages/upload_file_final.html")
   
def replace(nom_fich):
   with open(nom_fich, 'r') as file:
    # Read the content of the file
    content = file.read()

    # Replace "|" with ","
    modified_content = content.replace('|', ',')
   nom_fich_modif=nom_fich+'_modified'
   # Open the CDR file for writing
   with open(nom_fich_modif, 'w') as file:
    # Write the modified content back to the file
    file.write(modified_content)
   return nom_fich_modif
    
def read_fich(nom_fich):
   import pandas as pd
   import numpy as np
   n=0
   nom_modif=replace(nom_fich)
   cdr_file = pd.read_csv(nom_modif)
   # cdr_file.columns
   cdr18=cdr_file["Intrunk"].values
   cdr19=cdr_file["Outtrunk"].values
   cdr18=cdr18.reshape(-1,1)
   cdr19=cdr19.reshape(-1,1)
   print(cdr18)
   print(cdr19)
   ooredoo_out=np.count_nonzero(np.equal(cdr19, 'OUTODOO'))
   orange_out=np.count_nonzero(np.equal(cdr19, 'OUTORGO'))
   ooredoo_in=np.count_nonzero(np.equal(cdr18, 'INORDI'))
   orange_in=np.count_nonzero(np.equal(cdr18, 'INORGI'))
   print(ooredoo_out)
   print(orange_out)
   print(ooredoo_in)
   print(orange_in)
   ooredoo=Ooredoo(in_OO=ooredoo_in,out_OO=ooredoo_out)
   orange=Orange(in_OR=orange_in,out_OR=orange_out)
   ooredoo.save()
   orange.save()
   # print(cdr18.shape[0])
   # print(cdr18[5][0])
   # for i in range(int(cdr19.shape[0])):
   #    if str(cdr19[i][0]) == "OUTODOO":
   #       n=n+1
   # print(n)
   


def send_files(request):
    if request.method == "POST" :
        name = request.POST.get('filename', None)
        myfile = request.FILES.getlist('uploadfoles')
        nomfich=myfile
        #print(nomfich[0])
        try:
         myuploadfile(myfiles=nomfich[0]).save()
        except OperationalError as e:
           print(e)
        read_fich(str(ss.MEDIA_ROOT)+'\\'+str(nomfich[0]))
        
      #   print(nomfich1)
      #   for f in myfile:
      
        
        
    return redirect("home")