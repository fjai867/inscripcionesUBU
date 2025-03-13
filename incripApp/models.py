from django.db import models

class Competicion(models.Model):
    idPrueba = models.AutoField(primary_key=True)  # Clave primaria automática
    nomPrueba = models.CharField(max_length=250)
    nombre = models.BooleanField()
    apellido1 = models.BooleanField()
    apellido2 = models.BooleanField()
    ano = models.BooleanField()
    categoria = models.BooleanField()
    club = models.BooleanField()
    fechanac = models.BooleanField()
    sexo = models.BooleanField()
    centroescolar = models.BooleanField()
    prueba1 = models.BooleanField()
    prueba2 = models.BooleanField()
    prueba3 = models.BooleanField()
    fechafin = models.DateTimeField()

    def __str__(self):
        return self.nomPrueba  # Para mostrar el nombre en el admin de Django

class Atleta(models.Model):
    idAtleta = models.AutoField(primary_key=True)  # Clave primaria automática para Atleta
    competicion = models.ForeignKey(Competicion, on_delete=models.CASCADE)  # Relación uno a muchos
    nom = models.CharField(max_length=50,null=False,blank=False)
    ape1 = models.CharField(max_length=50,null=False,blank=False)
    ape2 = models.CharField(max_length=50,null=False,blank=False)
    ano = models.CharField(max_length=4,null=True,blank=True)
    categoria = models.CharField(max_length=6,null=True,blank=True)
    club = models.CharField(max_length=20,null=True,blank=True)
    fechanac = models.DateField(null=True,blank=True)
    sexo = models.CharField(max_length=9,null=True,blank=True)
    centroescolar = models.CharField(max_length=50,null=True,blank=True)
    prueba1 = models.CharField(max_length=30,null=False,blank=False)
    prueba2 = models.CharField(max_length=30,null=True,blank=True)
    prueba3 = models.CharField(max_length=30,null=True,blank=True)

    def __str__(self):
        return f"{self.nom} {self.ape1}"  # Para mostrar nombre y apellido en el admin
    
class Documento(models.Model):
    fechagrab=models.DateTimeField(auto_now_add=True)
    competicion = models.ForeignKey(Competicion, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    archivo_pdf = models.FileField(upload_to='pdfs/')  # 'pdfs/' es la carpeta donde se guardarán los archivos

    def __str__(self):
        return self.titulo