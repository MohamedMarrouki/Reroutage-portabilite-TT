from django.shortcuts import render,redirect
from . models import *
from .forms import *
from django.conf import settings as ss
from django.db import OperationalError
from django.db.models import Sum
from django.contrib import auth
from django.utils import timezone
import csv
from django.core.files.storage import default_storage
from datetime import datetime


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
   #return render(request,"pages/upload_file_final.html")
   
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
   
def somme():
   total_in_oo = Ooredoo.objects.aggregate(total_in_oo=Sum('in_OO'))
   total_out_oo = Ooredoo.objects.aggregate(total_out_oo=Sum('out_OO'))
   sum_of_in_oo = total_in_oo['total_in_oo']
   sum_of_out_oo = total_out_oo['total_out_oo']
   total_in_or = Orange.objects.aggregate(total_in_or=Sum('in_OR'))
   total_out_or = Orange.objects.aggregate(total_out_or=Sum('out_OR'))
   sum_of_in_or = total_in_or['total_in_or']
   sum_of_out_or = total_out_or['total_out_or']
   print(int(sum_of_in_or))
   print(int(sum_of_out_or))
   print(int(sum_of_in_oo))
   print(int(sum_of_out_oo))
   return sum_of_in_oo,sum_of_out_oo,sum_of_in_or,sum_of_out_or

def chart(request):
   oo_in=somme()[0]
   oo_out=somme()[1]
   or_in=somme()[2]
   or_out=somme()[3]
   op_in_out_list = ['Ooredoo In', 'Ooredoo Out', 'Orange In', 'Orange Out']
   number_list = [oo_in, oo_out, or_in, or_out]
   user = auth.get_user(request)
   if user.is_authenticated:
        nom_utilisateur = user.username
        email_utilisateur = user.email
        nom = user.last_name + " " + user.first_name
   context = {'op_in_out_list':op_in_out_list, 'number_list':number_list,
              'nom_utilisateur': nom_utilisateur,
               'email_utilisateur': email_utilisateur,
               'nom': nom}
   return render(request, 'pages/chart.html', context)
   

def send_files(request):
    if request.method == "POST" :
        name = request.POST.get('filename', None)
        myfile = request.FILES.getlist('uploadfoles')
        nomfich=myfile
        #print(nomfich[0])
        try:
           uploadfile(fileuploaded=nomfich[0]).save()
        except OperationalError as e:
           print(e)
        dt=timezone.localtime()
        nom_modif=replace(str(ss.MEDIA_ROOT)+'\\'+str(nomfich[0]))
        index = nom_modif.rfind('\\')
        sous_chaine = nom_modif[index+1:] 
        print(sous_chaine)
        exists = myuploadfile.objects.filter(myfiles=sous_chaine).exists()
        if exists==False:
         upf=myuploadfile(myfiles=sous_chaine,date_upload=dt)
         try:
            upf.save()
         except OperationalError as e:
            print(e)
         file = default_storage.open(nom_modif)
      #   print(file)
         decoded_file = file.read().decode('utf-8').splitlines()
         reader = csv.DictReader(decoded_file)
         file_upload = myuploadfile.objects.get(id=upf.id)
      #   print(file_upload)
      #   print(upf.id)
      # A number|calledMNPInfo&Bnumber|||origine trafic|callday|calltime|||duration|ALL|Calltype|callreference|pulse|node|||Intrunk|Outtrunk|
         for row in reader:
           date_string = row['callday']  # Example date string in DD-MM-YYYY format
           date_object = datetime.strptime(date_string, '%d-%m-%Y')
           converted_date_string = date_object.strftime('%Y-%m-%d')
            # Création d'une instance du modèle LigneCSV avec les données du CSV
           ligne_csv = Ligne_fichier(
                  file_upload=file_upload,
                  Anumber=row['A number'],
                  Bnumber=row['calledMNPInfo&Bnumber'],
                  origine_trafic=row['origine trafic'],
                  call_day=converted_date_string,
                  call_time=row['calltime'],
                  call_duration=row['duration'],
                  ALL=row['ALL'],
                  Calltype=row['Calltype'],
                  callreference=row['callreference'],
                  pulse=row['pulse'],
                  node=row['node'],
                  Intrunk=row['Intrunk'],
                  Outtrunk=row['Outtrunk']
               )
           ligne_csv.save()
           context = {'exists':exists}
        else:
           print('existe')
           context = {'exists':exists}
      #   read_fich(str(ss.MEDIA_ROOT)+'\\'+str(nomfich[0]))
      #   somme()
        
   #    #   print(nomfich1)
   #    #   for f in myfile:
            
    return render(request, 'pages/upload_file_final.html', context)
 
 
def filtrer_produits(request):
   Lignef = Ligne_fichier.objects.all()
   day=request.POST.get('call_day')
   origin=request.POST.get('origin')
   trunk=request.POST.get('trunk')
   user = auth.get_user(request)
   if user.is_authenticated:
        nom_utilisateur = user.username
        email_utilisateur = user.email
        nom = user.last_name + " " + user.first_name
   if(trunk=='OUTORGO' or trunk=='OUTODOO'):
      test='out'
   elif(trunk=='INORDI' or trunk=='INORGI'):
      test='in'
   else:
      test='all' 
   
   if(str(origin).lower()=='international' ):
      if(test=='out'):
         Lignes = Lignef.filter(call_day=day,origine_trafic='international',Outtrunk=trunk)
         context = {
         'form': FiltreForm,
         'ligne':Lignes,
              'nom_utilisateur': nom_utilisateur,
               'email_utilisateur': email_utilisateur,
               'nom': nom
         }
      elif(test=='in'):
         Lignes = Lignef.filter(call_day=day,origine_trafic='international',Intrunk=trunk)
         context = {
         'form': FiltreForm,
         'ligne':Lignes,
              'nom_utilisateur': nom_utilisateur,
               'email_utilisateur': email_utilisateur,
               'nom': nom
         }
      else:
         Lignes = Lignef.filter(call_day=day,origine_trafic='international')
         context = {
         'form': FiltreForm,
         'ligne':Lignes
         }
   elif(str(origin).lower()=='national'):
      if(test=='out'):
         Lignes = Lignef.filter(call_day=day,Outtrunk=trunk).exclude(origine_trafic='international')
         context = {
         'form': FiltreForm,
         'ligne':Lignes,
              'nom_utilisateur': nom_utilisateur,
               'email_utilisateur': email_utilisateur,
               'nom': nom
         }
      elif(test=='in'):
         Lignes = Lignef.filter(call_day=day,Intrunk=trunk).exclude(origine_trafic='international')
         context = {
         'form': FiltreForm,
         'ligne':Lignes,
              'nom_utilisateur': nom_utilisateur,
               'email_utilisateur': email_utilisateur,
               'nom': nom
         }
      else:
         Lignes = Lignef.filter(call_day=day).exclude(origine_trafic='international')
         context = {
         'form': FiltreForm,
         'ligne':Lignes,
              'nom_utilisateur': nom_utilisateur,
               'email_utilisateur': email_utilisateur,
               'nom': nom
         }
   else:
      context = {
         'form': FiltreForm,
         'ligne':Lignef,
              'nom_utilisateur': nom_utilisateur,
               'email_utilisateur': email_utilisateur,
               'nom': nom
         }
      

   return render(request, 'pages/filtre_CDR.html', context)