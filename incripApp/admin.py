from django.contrib import admin

# Register your models here.
from .models import Competicion,Atleta

admin.site.register(Competicion)
admin.site.register(Atleta)
