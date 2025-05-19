from django.shortcuts import render, HttpResponse, redirect,HttpResponseRedirect,get_object_or_404
from incripApp.models import Competicion, Atleta, Documento
from django.views.generic import ListView,DeleteView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from .forms import LoginForm
from openpyxl import Workbook
from django.http import FileResponse,Http404
#importacion para que la vista solo se pueda entrar a traves de login
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date

import os
from django.conf import settings








def vista(request, idPrueb):
    
    miRegi=Competicion.objects.get(idPrueba=idPrueb)  
    
    
    
    contexto={'regCompeticion':miRegi}
    try:
        if request.method == 'POST':
            
            errores={}
            if request.POST:
                nombre = request.POST.get('nom')
                ape1=request.POST.get('ape1')
                ape2=request.POST.get('ape2')
                ano=request.POST.get('ano')
                club=request.POST.get('club')
                categoria=request.POST.get('cat')
                fechanac=request.POST.get('fechanac')
                sexo=request.POST.get('sexo')
                cescolar=request.POST.get('cescolar')

                pr1=request.POST.get('pr1')
                pr2=request.POST.get('pr2')
                pr3=request.POST.get('pr3')

                #errores de los campos fijos siempre activos
                if not nombre:
                    errores['nom'] = "El nombre es obligatorio."
                if not ape1:
                    errores['ape1'] = "El primer apellido es obligatorio."
                if not ape2:
                    errores['ape2'] = "El segundo apellido es obligatorio."
                if not pr1:
                    errores['pr1'] = "Debes porner al menos una prueba."

                #errores de los campos que pueden estar habilitados
                if miRegi.ano:
                    if not ano:
                        errores['ano'] = "Debes porner el año."

                if miRegi.club:
                    if not club:
                        errores['club'] = "Debes porner el club."

                if miRegi.fechanac:
                    if not fechanac:
                        errores['fecha'] = "Debes porner la fecha de nacimiento."

                if miRegi.centroescolar==True:
                    if not cescolar:
                        errores['cescol'] = "Debes porner el centro escolar." 

                if miRegi.prueba2:
                    if not pr2:
                        errores['pr2'] = "Pon NO si no te apuntas a la 2ª prueba" 

                if miRegi.prueba3:
                    if not pr3:
                        errores['pr3'] = "Pon NO si no te apuntas a la 3ª prueba" 

                if errores:
                    return render(request, 'exito.html', {'mensaje':'Hay algún error en el formlario','erroress': errores.values()}) # Pasar errores y datos para repopular el formulario
                else:    
                    # Crea una instancia del modelo y guarda los datos
                    nuevo_registro = Atleta(competicion=miRegi,nom=nombre, ape1=ape1, ape2=ape2, ano=ano,categoria=categoria,club=club,fechanac=fechanac,sexo=sexo,centroescolar=cescolar,prueba1=pr1,prueba2=pr2,prueba3=pr3)
                    nuevo_registro.save()

                # Redirigir a una página de éxito o mostrar un mensaje
                return render(request, 'exito.html', {'mensaje': 'Datos guardados correctamente','mensaje2':'te has apuntado en: ','regnuevo': nuevo_registro})
                            
        else:
            return render(request,"home2.html",contexto)
    except:
        return render(request, 'exito.html', {'mensaje': 'Ha ocurrdo algun problema no estas apuntado', 'mensaje2':'intentalo de nuevo'})

        
def portada(request):
    return render(request,"home.html")



    

class Competiciones(ListView):
    model = Competicion
    template_name = 'compet.html'  # Especifica el nombre del template HTML
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(fechafin__gte=date.today())
    
class borrarCom(DeleteView):
    model = Competicion
    template_name = 'borrarcom.html'
    success_url = reverse_lazy('generar_excel')  # Reemplaza con la URL de la lista de modelos
    
    


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['username'] = "Administrador"
                 #envia a la lista de competicionees para exporta excel
                return HttpResponseRedirect(reverse_lazy('generar_excel'))
            else:
                form.add_error(None, 'Nombre de usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


class generar_excel(LoginRequiredMixin, ListView):
    model = Competicion
    template_name = 'generar.html'  # Especifica el nombre del template HTML
    context_object_name = 'object_list'  # Opcional: Cambia el nombre de la variable
    




def exportar_excel(request, idPrueb):
    # Filtra los atletas por la competición
    atletas = Atleta.objects.filter(competicion=idPrueb)

    # obtenemos el registro idPureba de competicion
    miRegi = Competicion.objects.get(idPrueba=idPrueb)

    # Lista de todos los campos posibles (debe coincidir con los datos que quieres exportar)
    all_fields = ['nom', 'ape1', 'ape2', 'ano', 'categoria', 'club', 'fechanac', 'sexo', 'centroescolar', 'prueba1', 'prueba2', 'prueba3']
    header_map = {
        'nom': 'Nombre',
        'ape1': 'Apellido1',
        'ape2': 'Apellido2',
        'ano': 'Año',
        'categoria': 'Categoría',
        'club': 'Club',
        'fechanac': 'Fechanac',
        'sexo': 'sexo',
        'centroescolar': 'centro-escolar',
        'prueba1': 'Prueba 1',
        'prueba2': 'Prueba 2',
        'prueba3': 'Prueba 3',
    }
    categ = ["sub-8", "sub-10", "sub-12", "sub-14", "sub-16", "sub-18", "sub-20", "sub-23", "senior", "master"]
    sex = ["masculino", "femenino"]

    # Identificar campos con todos los valores nulos
    null_fields = set()
    for field_name in all_fields:
        all_null = True
        for atleta in atletas:
            if getattr(atleta, field_name) is not None:
                all_null = False
                break
        if all_null and atletas.exists():  # Solo considerar si hay atletas
            null_fields.add(field_name)

    # Crear encabezados dinámicamente
    encabezados = [header_map[field] for field in all_fields if field not in null_fields]

    # Crea un nuevo libro de Excel y una hoja
    wb = Workbook()
    ws = wb.active
    ws.append(encabezados)

    # Escribe los datos de los atletas en las filas
    for atleta in atletas:
        fila_data = []
        for field_name in all_fields:
            if field_name not in null_fields:
                value = getattr(atleta, field_name)
                if field_name == 'categoria' and value is not None:
                    fila_data.append(categ[int(value)])
                elif field_name == 'sexo' and value is not None:
                    fila_data.append(sex[int(value)])
                else:
                    fila_data.append(value)
        ws.append(fila_data)

    # Crea la respuesta HTTP con el archivo Excel
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="atletas_{miRegi.nomPrueba[:15]}.xlsx"'

    # Guarda el libro de Excel en la respuesta
    wb.save(response)

    return response


    

def ver_pdf(request, pk):
    try:
        documento = Documento.objects.get(competicion=pk)
        if documento.archivo_pdf:
            return FileResponse(open(documento.archivo_pdf.path, 'rb'), content_type='application/pdf')
        else:
            return render(request, 'falloPDF.html', {'mensaje': 'El documento no tiene archivo PDF asociado'})
    except Documento.DoesNotExist:
        #raise Http404("Fallo. Algo no ha salido bien. Intentelo de nuevo")
        return render(request, 'falloPDF.html', {'mensaje': 'El documento no tiene archivo PDF asociado'})
    


def Aviso_Legal(request):
    """
    Vista para mostrar el archivo Aviso_Legal.pdf.
    """
    ruta_archivo = os.path.join(settings.MEDIA_ROOT, 'pdf', 'Aviso_Legal.pdf')

    try:
        with open(ruta_archivo, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename="Aviso_Legal.pdf"'
            return response
    except FileNotFoundError:
        return HttpResponse("El archivo PDF no se encontró.", status=404)
    
def condiciones_pdf(request):
    """
    Vista para mostrar el archivo Terminos_y_condiciones.pdf.
    """
    ruta_archivo = os.path.join(settings.MEDIA_ROOT, 'pdf', 'Terminos_y_condiciones.pdf')

    try:
        with open(ruta_archivo, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename="Terminos_y_condiciones.pdf"'
            return response
    except FileNotFoundError:
        return HttpResponse("El archivo PDF no se encontró.", status=404)
    

def privacidad_pdf(request):
    """
    Vista para mostrar el archivo Politica_de_privacidad.pdf.
    """
    ruta_archivo = os.path.join(settings.MEDIA_ROOT, 'pdf', 'Politica_de_privacidad.pdf')

    try:
        with open(ruta_archivo, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename="Politica_de_privacidad.pdf"'
            return response
    except FileNotFoundError:
        return HttpResponse("El archivo PDF no se encontró.", status=404)
    
def politica_cookies_pdf(request):
    """
    Vista para mostrar el archivo Politica_de_Cookies.pdf.
    """
    ruta_archivo = os.path.join(settings.MEDIA_ROOT, 'pdf', 'Politica_de_Cookies.pdf')

    try:
        with open(ruta_archivo, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename="Politica_de_Cookies.pdf"'
            return response
    except FileNotFoundError:
        return HttpResponse("El archivo PDF no se encontró.", status=404)
    


    
def logout_view(request):
    """
    Vista para cerrar la sesión del usuario.
    """
    logout(request)
    return redirect('portada')  # Redirige a la página de inicio


def ver_inscritos(request, pk):
    """
    Vista para mostrar los datos de los atletas inscritos en una competición.
    """
    atletas = Atleta.objects.filter(competicion=pk)
    return render(request, 'inscritos.html', {'atletas': atletas})
    
    