from django.shortcuts import render

# Create your views here.
def home(request):
   return render(request, 'pages/login.html')
   #return HttpResponse('bonjour')
   
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
   nom_modif=replace(nom_fich)
   cdr_file = pd.read_csv(nom_modif)
   # cdr_file.columns
   cdr18=cdr_file["r"].values
   cdr19=cdr_file["s"].values
   cdr18=cdr18.reshape(-1,1)
   cdr19=cdr19.reshape(-1,1)
