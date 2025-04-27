"""
URL configuration for inscripciones project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from .views import Competiciones, generar_excel,borrarCom

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.portada, name='portada'),
    path('Competicion',Competiciones.as_view(), name='Competicion'),
    path('vista/<int:idPrueb>/',views.vista, name='vista'),
    path("borrarCom/<int:pk>/",borrarCom.as_view(), name='borrarCom'),
    path("login/",views.login_view, name='login'),
    path("generar_excel/",generar_excel.as_view(), name='generar_excel'),
    path("exportar_excel/<int:idPrueb>/",views.exportar_excel, name='exportar_excel'),
    path('verpdf/<int:pk>/',views.ver_pdf, name='verpdf'),
    path('aviso/',views.Aviso_Legal, name='aviso'),
    path('cooki/',views.politica_cookies_pdf, name='cooki'),
    path('priva/',views.privacidad_pdf, name='priva'),
    path('condi/',views.condiciones_pdf, name='condi'),
    path('logout/', views.logout_view, name='logout'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

