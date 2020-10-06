from django import forms

from core.models import Reserva, Quarto


class QuartoChangeForm(forms.ModelForm):
    class Meta:
        model = Quarto
        fields = (
            'name',
            'endereco',
            'tratar',
            'telefone',
            'description',
            'imagem',
            'color',
        )


class ReservaChangeForm(forms.ModelForm):
    start_date = forms.DateField(input_formats=['%d/%m/%Y'])
    end_date = forms.DateField(input_formats=['%d/%m/%Y'])

    class Meta:
        model = Reserva
        fields = (
            'quarto',
            'name',
            'telefone',
            'status',
            'start_date',
            'end_date',
            'comprovante',
        )
