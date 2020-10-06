import datetime
import random

from django.core.exceptions import ValidationError
from django.utils import timezone
from model_mommy import mommy

from core.models import Reserva, Quarto

start_date = timezone.now()
end_date = start_date + timezone.timedelta(days=800)
quarto_list = Quarto.objects.all()

names = [
    'Reserva feriado', 'Fim de semana', 'Férias',
]


def random_date(start=start_date, end=end_date):
    return start + datetime.timedelta(seconds=random.randint(0, int((end - start).total_seconds())))


# def random_time():
#     start = random.randint(0, 16)
#     end = random.randint(start, 22)
#     return str(start) + ':00', str(end) + ':00'


def create_reservas(quartos, quantity=1):
    reservas = []
    for i in range(0, quantity):
        name = random.choice(names)
        quarto = random.choice(quartos)
        date = random_date()
        start, end = random_time()
        try:
            reservas.append(mommy.make(
                Reserva,
                date=date,
                name=name,
                quarto=quarto,
                start=start,
                end=end
            ))
        except ValidationError:
            pass
    return reservas
