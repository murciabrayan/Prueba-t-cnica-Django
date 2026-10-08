from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import AlertaForm, CancelarParadaForm, ParadaForm
from .models import Alerta, Parada


def tiene_rol(usuario, rol):
    return usuario.groups.filter(name=rol).exists()


def exigir_rol(usuario, rol):
    # Si el usuario no tiene el rol, Django responde 403 (prohibido)
    if not tiene_rol(usuario, rol):
        raise PermissionDenied


def mostrar_errores(request, form):
    for campo, errores in form.errors.items():
        for error in errores:
            if campo == '__all__':
                messages.error(request, error)
            else:
                messages.error(request, f'{campo}: {error}')


@login_required
def inicio(request):
    es_operario = tiene_rol(request.user, 'Operario')
    es_supervisor = tiene_rol(request.user, 'Supervisor')
    es_jefe = tiene_rol(request.user, 'Jefe')

    # El operario solo ve sus alertas; supervisor y jefe ven todas
    if es_operario:
        alertas = Alerta.objects.filter(usuario=request.user).order_by('-fecha')
    elif es_supervisor or es_jefe:
        alertas = Alerta.objects.all().order_by('-fecha')
    else:
        alertas = Alerta.objects.none()

    # Solo supervisor y jefe ven las paradas
    if es_supervisor or es_jefe:
        paradas = Parada.objects.all().order_by('-inicio')
    else:
        paradas = Parada.objects.none()

    return render(request, 'maquinas/inicio.html', {
        'es_operario': es_operario,
        'es_supervisor': es_supervisor,
        'es_jefe': es_jefe,
        'alertas': alertas,
        'paradas': paradas,
        'alerta_form': AlertaForm(),
        'parada_form': ParadaForm(),
    })


@login_required
@require_POST
def crear_alerta(request):
    exigir_rol(request.user, 'Operario')
    form = AlertaForm(request.POST)
    if form.is_valid():
        alerta = form.save(commit=False)
        alerta.usuario = request.user
        alerta.save()
        messages.success(request, 'Alerta registrada.')
    else:
        mostrar_errores(request, form)
    return redirect('inicio')


@login_required
@require_POST
def editar_alerta(request, pk):
    exigir_rol(request.user, 'Supervisor')
    alerta = get_object_or_404(Alerta, pk=pk)
    form = AlertaForm(request.POST, instance=alerta)
    if form.is_valid():
        form.save()
        messages.success(request, f'Alerta {pk} actualizada.')
    else:
        mostrar_errores(request, form)
    return redirect('inicio')


@login_required
@require_POST
def crear_parada(request):
    exigir_rol(request.user, 'Supervisor')
    form = ParadaForm(request.POST)
    if form.is_valid():
        parada = form.save(commit=False)
        parada.usuario = request.user
        parada.save()
        messages.success(request, 'Parada registrada.')
    else:
        mostrar_errores(request, form)
    return redirect('inicio')


@login_required
@require_POST
def cancelar_parada(request, pk):
    exigir_rol(request.user, 'Jefe')
    parada = get_object_or_404(Parada, pk=pk)
    form = CancelarParadaForm(request.POST)

    if not form.is_valid():
        mostrar_errores(request, form)
    elif parada.cancelada_en:
        # Ya estaba cancelada: no se cambia nada
        messages.warning(request, f'La parada {pk} ya estaba cancelada.')
    else:
        parada.cancelada_por = request.user
        parada.cancelada_en = timezone.now()
        parada.motivo_cancelacion = form.cleaned_data['motivo_cancelacion']
        parada.save()
        messages.success(request, f'Parada {pk} cancelada.')
    return redirect('inicio')
