from django.contrib import admin

# Register your models here.
from .models import Competicion,Atleta,Documento

admin.site.register(Competicion)
admin.site.register(Atleta)
admin.site.register(Documento)
