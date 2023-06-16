from django.db import models

# Create your models here.
class myuploadfile(models.Model):
    myfiles = models.FileField(upload_to='')

#     def __str__(self):
#         return self.f_name

class Ooredoo(models.Model):
    # name_OO = models.CharField(max_length=500, null=True)
    in_OO = models.IntegerField(null=True)
    out_OO = models.IntegerField(null=True)
    
    
class Orange(models.Model):
    # name_OR = models.CharField(max_length=500, null=True)
    in_OR = models.IntegerField(null=True)
    out_OR = models.IntegerField(null=True)
