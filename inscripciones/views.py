from django.shortcuts import render, HttpResponse
from incripApp.models import Competicion, Atleta
from django.views.generic import ListView


def vista(request, idPrueb):
    
    miRegi=Competicion.objects.get(idPrueba=idPrueb)  
    
    
    
    contexto={'regCompeticion':miRegi}
    if request.method == 'POST':
        if request.POST:
            #nombre = request.POST.get('nom')
            #ape1=request.POST.get('ape1')
            #ape2=request.POST.get('ape2')
            #ano=request.POST.get('ano')
            #club=request.POST.get('club')
            #categoria=request.POST.get('cat')
            #pr1=request.POST.get('pr1')
            #pr2=request.POST.get('pr2')
            #pr3=request.POST.get('pr3')
            pass
            # Crea una instancia del modelo y guarda los datos
            #nuevo_registro = Atleta(nom=nombre, ape1=ape1, ape2=ape2, ano=ano,categoria=categoria,club=club,prueba1=pr1,prueba2=pr2,prueba3=pr3)
            #nuevo_registro.save()

            # Redirigir a una página de éxito o mostrar un mensaje
            #return render(request, 'exito.html', {'mensaje': 'Datos guardados correctamente'})
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
    