from django import template

register = template.Library()

translation_dict = {
    'True': 'Sim',
    'False': 'Não',
    'Name': 'Nome',
    'Slug': 'Slug',
    'Description': 'Descrição',
    'Active': 'Ativa',
    'Color': 'Cor',
    'Quarto': 'Quarto',
    'Scheduled': 'Agendada',
    'Canceled': 'Cancelada',
    'Status': 'Status',
    'Telefone': 'Telefone',
    'Start date': 'Data inícial',
    'End date': 'Data Final',
    'Comprovante': 'Comprovante'

}


@register.filter(name='translation')
def translation(value):
    return translation_dict.get(str(value), '')
