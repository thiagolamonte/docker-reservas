from django.contrib import admin

from core.models import Reserva, Quarto


@admin.register(Quarto)
class QuartoAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    list_filter = ('date_added', 'date_changed')
    search_fields = ('name',)
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('name', 'quarto', 'telefone', 'status', 'start_date', 'end_date', 'comprovante')
    list_filter = ('quarto', 'status', 'start_date', 'date_added', 'date_changed')
    search_fields = ('name',)
    ordering = ('start_date',)
