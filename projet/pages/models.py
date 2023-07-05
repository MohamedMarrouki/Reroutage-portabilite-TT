from django.db import models

# Create your models here.
class myuploadfile(models.Model):
    myfiles = models.FileField()
    date_upload=models.DateTimeField()

#     def __str__(self):
#         return self.f_name

class uploadfile(models.Model):
    fileuploaded = models.FileField(upload_to='')

class Ooredoo(models.Model):
    # name_OO = models.CharField(max_length=500, null=True)
    in_OO = models.IntegerField(null=True)
    out_OO = models.IntegerField(null=True)
    
    
class Orange(models.Model):
    # name_OR = models.CharField(max_length=500, null=True)
    in_OR = models.IntegerField(null=True)
    out_OR = models.IntegerField(null=True)

    
class Ligne_fichier(models.Model):
    file_upload=models.ForeignKey(myuploadfile,on_delete=models.CASCADE)
    Anumber=models.IntegerField(null=True)
    Bnumber=models.IntegerField(null=True)
    origine_trafic=models.CharField(max_length=255,null=True)
    call_day=models.DateField(null=True)
    call_time=models.TimeField(null=True)
    call_duration=models.IntegerField(null=True)
    ALL=models.CharField(max_length=20,null=True)
    Calltype=models.CharField(max_length=20,null=True)
    callreference=models.IntegerField(null=True)
    pulse=models.IntegerField(null=True)
    node=models.CharField(max_length=255,null=True)
    Intrunk=models.CharField(max_length=255,null=True)
    Outtrunk=models.CharField(max_length=255,null=True)
    
class Country(models.Model):
    Pays=models.CharField(max_length=100)
    Code=models.CharField(max_length=10)
    call_count=models.IntegerField(null=True)

    
    
    
    
    
    
    
    