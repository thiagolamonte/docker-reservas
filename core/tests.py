from copy import deepcopy

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestQuartoCreation:

    @pytest.fixture
    def quartos_endpoint(self):
        return reverse('api:quarto-list')

    @pytest.fixture
    def payload_quarto_creation(self):
        return {
            "name": "Quarto Simples",
            "slug": "quarto-simples",
            "description": "quarto com cama e televisão para até 2 pessoas",
            "color": "green",
        }

    def test_should_create_quarto(self, quartos_endpoint, public_client, payload_quarto_creation):
        response = public_client.post(
            quartos_endpoint, data=payload_quarto_creation, format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestQuartoPayload:

    @pytest.fixture
    def quartos_endpoint(self):
        return reverse('api:quarto-list')

    @pytest.fixture
    def payload_quarto_list(self, quarto_one):
        return [
            {
                "id": 1,
                "name": "Quarto Familia",
                "slug": "quarto-familia",
                "description": "Quarto para até 6 pessoas",
                "color": "red",
            }
        ]

    def test_should_return_right_payload(self, quartos_endpoint, public_client, payload_quarto_list):
        response = public_client.get(quartos_endpoint)
        json_response = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert json_response == payload_quarto_list


@pytest.mark.django_db
class TestReservaCreation:

    @pytest.fixture
    def reserva_endpoint(self):
        return reverse('api:reserva-list')

    @pytest.fixture
    def payload_reserva_creation(self):
        return {
            "name": "Reserva final de semana",
            "quarto": 1,
            "description": "Dois adultos e uma criança",
            "status": "scheduled",
            "date": "26/12/2018",
            "start": "14:00",
            "end": "16:00"
        }

    @pytest.fixture
    def payload_reserva_creation_with_different_date_format(self):
        return {
            "name": "Reserva final de semana",
            "quarto": 1,
            "description": "Dois adultos e uma criança",
            "status": "scheduled",
            "date": "26-12-2018",
            "start": "14:00",
            "end": "16:00"
        }

    @pytest.fixture
    def payload_reserva_creation_with_different_time_format(self):
        return {
            "name": "Reserva final de semana",
            "quarto": 1,
            "description": "Dois adultos e uma criança",
            "status": "scheduled",
            "date": "26-12-2018",
            "start": "14:00",
            "end": "16:00"
        }

    @pytest.fixture
    def payload_conflicting_reserva_creation(self, payload_reserva_creation):
        payload = deepcopy(payload_reserva_creation)
        payload['start'] = '12:00'
        payload['end'] = '18:00'
        return payload

    @pytest.fixture
    def payload_conflicting_reserva_creation_with_canceled_status(self, payload_conflicting_reserva_creation):
        payload = deepcopy(payload_conflicting_reserva_creation)
        payload['status'] = 'canceled'
        return payload

    @pytest.fixture
    def payload_end_greater_than_start_reserva_creation(self, payload_reserva_creation):
        payload = deepcopy(payload_reserva_creation)
        payload['start'] = '18:00'
        payload['end'] = '10:00'
        return payload

    def test_should_create_reserva(
            self, reserva_endpoint, public_client, payload_reserva_creation, quarto_one
    ):
        response = public_client.post(
            reserva_endpoint, data=payload_reserva_creation, format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_should_create_reserva_with_different_date_format(
            self, reserva_endpoint, public_client, payload_reserva_creation_with_different_date_format, quarto_one
    ):
        response = public_client.post(
            reserva_endpoint, data=payload_reserva_creation_with_different_date_format, format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_should_create_reserva_with_different_time_format(
            self, reserva_endpoint, public_client, payload_reserva_creation_with_different_time_format, quarto_one
    ):
        response = public_client.post(
            reserva_endpoint, data=payload_reserva_creation_with_different_time_format, format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_should_not_create_reserva_with_conflicting_time(
            self, reserva_endpoint, public_client, payload_conflicting_reserva_creation, reserva_one, quarto_one
    ):
        response = public_client.post(
            reserva_endpoint, data=payload_conflicting_reserva_creation, format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()['non_field_errors'][0] == 'Quarto {name} already booked in this period.'.format(
            name=quarto_one.name
        )

    def test_should_create_reserva_with_conflicting_time_but_canceled_status(
            self,
            reserva_endpoint,
            public_client,
            payload_conflicting_reserva_creation_with_canceled_status,
            reserva_one,
            quarto_one
    ):
        response = public_client.post(
            reserva_endpoint, data=payload_conflicting_reserva_creation_with_canceled_status, format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_should_not_create_reserva_with_end_greater_than_start(
            self, reserva_endpoint, public_client, payload_end_greater_than_start_reserva_creation, quarto_one
    ):
        response = public_client.post(
            reserva_endpoint, data=payload_end_greater_than_start_reserva_creation, format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()['non_field_errors'][0] == 'Start cannot be greater than end.'


@pytest.mark.django_db
class TestReservaPayload:

    @pytest.fixture
    def reserva_endpoint(self):
        return reverse('api:reserva-list')

    @pytest.fixture
    def payload_reserva_list(self, reserva_one):
        return [
            {
                "id": 1,
                "name": "Reserva feriado",
                "quarto": 1,
                "description": "Um casal",
                "status": "scheduled",
                "date": "26-12-2018",
                "start": "14:00:00",
                "end": "16:00:00",
            }
        ]

    def test_should_return_right_payload(self, reserva_endpoint, public_client, payload_reserva_list):
        response = public_client.get(reserva_endpoint)
        json_response = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert json_response == payload_reserva_list
