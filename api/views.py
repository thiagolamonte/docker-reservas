import logging

from django_filters import FilterSet, DateFilter
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from api.serializers import ReservaSerializer, QuartoSerializer
from core.models import Reserva, Quarto

logger = logging.getLogger('reservas')


class QuartoFilterSet(FilterSet):
    class Meta:
        model = Quarto
        fields = [
            'slug',
        ]


class ReservaFilterSet(FilterSet):
    start_date_gte = DateFilter(field_name='start_date', lookup_expr='gte')
    end_date_lte = DateFilter(field_name='end_date', lookup_expr='lte')

    class Meta:
        model = Reserva
        fields = [
            'quarto',
            'status',
            'start_date',
            'end_date',
            'start_date_gte',
            'end_date_lte',
        ]


class QuartoViewSet(viewsets.ModelViewSet):
    queryset = Quarto.objects.all()
    serializer_class = QuartoSerializer
    permission_classes = (AllowAny,)
    filterset_class = QuartoFilterSet


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = (AllowAny,)
    filterset_class = ReservaFilterSet
