from django.shortcuts import render, HttpResponse, redirect
from incripApp.models import Competicion, Atleta
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from .forms import LoginForm


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
            pr1=request.POST.get('pr1')
            pr2=request.POST.get('pr2')
            pr3=request.POST.get('pr3')
            
            # Crea una instancia del modelo y guarda los datos
            nuevo_registro = Atleta(competicion=miRegi,nom=nombre, ape1=ape1, ape2=ape2, ano=ano,categoria=categoria,club=club,prueba1=pr1,prueba2=pr2,prueba3=pr3)
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
    context_object_name = 'object_list'  # Opcional: Cambia el nombre de la variable de contexto


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('inicio')  # Reemplaza con la URL deseada
            else:
                form.add_error(None, 'Nombre de usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
    