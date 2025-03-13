from django.shortcuts import render, HttpResponse, redirect,HttpResponseRedirect,get_object_or_404
from incripApp.models import Competicion, Atleta, Documento
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from .forms import LoginForm
from openpyxl import Workbook
#importacion para que la vista solo se pueda entrar a traves de login
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date



def vista(request, idPrueb):
    
    miRegi=Competicion.objects.get(idPrueba=idPrueb)  
    
    
    
    contexto={'regCompeticion':miRegi}
    if request.method == 'POST':
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
            
            # Crea una instancia del modelo y guarda los datos
            nuevo_registro = Atleta(competicion=miRegi,nom=nombre, ape1=ape1, ape2=ape2, ano=ano,categoria=categoria,club=club,fechanac=fechanac,sexo=sexo,centroescolar=cescolar,prueba1=pr1,prueba2=pr2,prueba3=pr3)
            nuevo_registro.save()

            # Redirigir a una página de éxito o mostrar un mensaje
            return render(request, 'exito.html', {'mensaje': 'Datos guardados correctamente'})
        else:
            mensaje = "No se han enviado datos."
            #return render(request, 'formulario.html', {'mensaje': mensaje})
    else:
        return render(request,"home2.html",contexto)
    
def inicio(request):
    
    return HttpResponse ("estoy hasta los huevos")
    
    

class Competiciones(ListView):
    model = Competicion
    template_name = 'compet.html'  # Especifica el nombre del template HTML
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(fechafin__gte=date.today())
    
    


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
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
    miRegi=Competicion.objects.get(idPrueba=idPrueb)

    # Crea un nuevo libro de Excel y una hoja
    wb = Workbook()
    ws = wb.active

     

    # Escribe los encabezados de las columnas
    encabezados = ['Nombre', 'Apellido1', 'Apellido2', 'Año', 'Categoría', 'Club',''
    ''
    'Fechanac','sexo','centro-escolar', 'Prueba 1', 'Prueba 2', 'Prueba 3']
    ws.append(encabezados)

    # Escribe los datos de los atletas en las filas
    for atleta in atletas:
        fila = [
            atleta.nom,
            atleta.ape1,
            atleta.ape2,
            atleta.ano,
            atleta.categoria,
            atleta.club,
            atleta.fechanac,
            atleta.sexo,
            atleta.centroescolar,
            atleta.prueba1,
            atleta.prueba2,
            atleta.prueba3,
        ]
        ws.append(fila)

    # Crea la respuesta HTTP con el archivo Excel
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="atletas_{miRegi.nomPrueba[:10]}.xlsx"'

    # Guarda el libro de Excel en la respuesta
    wb.save(response)

    return response


# Vista para mostrar el pdf en el navegador sin descargar.
def vista_pdf(request, pk):
    
    document = get_object_or_404(Documento, competicion=pk)
    response = HttpResponse(document.archivo_pdf.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{document.archivo_pdf.name}"'
    return response

    