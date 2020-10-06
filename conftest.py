import pytest
from model_mommy import mommy
from rest_framework.test import APIClient


@pytest.fixture
def public_client():
    client = APIClient()
    return client


@pytest.fixture
def quarto_one():
    return mommy.make(
        'core.Quarto',
        name='Quarto Familia',
        slug='quarto-familia',
        description='Quarto para até 6 pessoas',
        color='red',
    )


@pytest.fixture
def quarto_two():
    return mommy.make('core.Quarto')


@pytest.fixture
def reserva_one(quarto_one):
    return mommy.make(
        'core.Reserva',
        name='Reserva final de semana',
        description='Dois adultos e uma criança',
        quarto=quarto_one,
        date='2018-12-26',
        status='scheduled',
        start='14:00',
        end='16:00',
    )


@pytest.fixture
def reserva_two(quarto_two):
    return mommy.make(
        'core.Reserva',
        room=quarto_two,
        date='2018-12-26',
        status='scheduled',
        start='14:00',
        end='16:00',
    )
