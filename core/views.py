from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from core.forms import ReservaChangeForm, QuartoChangeForm
from core.models import Reserva, Quarto


def index(request):
    return render(request, 'core/index.html')


def quarto_list(request):
    quartos = Quarto.objects.order_by('name')
    return render(request, 'core/quarto_list.html', {
        'quartos': quartos,
    })


def reserva_list(request):
    reservas = Reserva.objects.prefetch_related(
        'quarto',
    ).order_by('start_date')
    return render(request, 'core/reserva_list.html', {
        'reservas': reservas,
    })


def reserva_calendar(request):
    reservas = Reserva.objects.prefetch_related(
        'quarto',
    ).order_by('start_date')
    return render(request, 'core/reserva_calendar.html', {
        'reservas': reservas,
    })


def quarto_add(request):
    form = QuartoChangeForm()
    if request.method == 'POST':
        form = QuartoChangeForm(request.POST, request.FILES)
        if form.is_valid():
            quarto = form.save(commit=False)
            quarto.slug = slugify(quarto.name)
            quarto.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                extra_tags='success',
                message='Quarto {name} cadastrado com sucesso.'.format(
                    name=quarto.name
                )
            )
            return redirect('core:quarto-list')
    return render(request, 'core/quarto_change.html', {
        'form': form,
    })


def quarto_change(request, quarto_id):
    quarto = get_object_or_404(Quarto, id=quarto_id)
    form = QuartoChangeForm(instance=quarto)
    if request.method == 'POST':
        form = QuartoChangeForm(data=request.POST, instance=quarto)
        if form.is_valid():
            quarto = form.save(commit=False)
            quarto.slug = slugify(quarto.name)
            quarto.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                extra_tags='success',
                message='Quarto {name} editado com sucesso.'.format(
                    name=quarto.name
                )
            )
            return redirect('core:quarto-list')
    return render(request, 'core/quarto_change.html', {
        'form': form,
        'quarto': quarto,
    })


def reserva_add(request):
    quartos = Quarto.objects.all()
    form = ReservaChangeForm()
    if request.method == 'POST':
        form = ReservaChangeForm(request.POST, request.FILES)
        if form.is_valid():
            reserva = form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                extra_tags='success',
                message='Reserva {name} adcionada com sucesso.'.format(
                    name=reserva.name
                )
            )
            return redirect('core:reserva-list')
    return render(request, 'core/reserva_change.html', {
        'form': form,
        'quartos': quartos,
    })


def reserva_change(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    quartos = Quarto.objects.all()
    form = ReservaChangeForm(instance=reserva)
    if request.method == 'POST':
        form = ReservaChangeForm(data=request.POST, instance=reserva)
        if form.is_valid():
            reserva.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                extra_tags='success',
                message='Reserva {name} editada com sucesso.'.format(
                    name=reserva.name
                )
            )
            return redirect('core:reserva-list')
    return render(request, 'core/reserva_change.html', {
        'form': form,
        'quartos': quartos,
        'reserva': reserva,
    })

