import logging

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.models import Reserva, Quarto

logger = logging.getLogger('reservas')


class QuartoSerializer(ModelSerializer):

    class Meta:
        model = Quarto
        fields = (
            'id',
            'name',
            'endereco',
            'tratar',
            'telefone',
            'description',
            'imagem',
            'color',
        )

    def create(self, validated_data):
        logger.info('Creating quarto "{name}".'.format(
            name=validated_data.get('name')
        ))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        logger.info('Updating quarto "{name}".'.format(
            name=instance.name
        ))
        return super().update(instance, validated_data)


class ReservaSerializer(ModelSerializer):
    start_date = serializers.DateField(format='%d-%m-%Y', input_formats=['%d-%m-%Y', '%d/%m/%Y'])
    end_date = serializers.DateField(format='%d-%m-%Y', input_formats=['%d-%m-%Y', '%d/%m/%Y'])

    class Meta:
        model = Reserva
        fields = (
            'id',
            'name',
            'quarto',
            'telefone',
            'status',
            'start_date',
            'end_date',
        )

    def create(self, validated_data):
        logger.info(
            'Creating reserva "{reserva_name}" for quarto "{quarto_name}".'.format(
                reserva_name=validated_data.get('name'),
                quarto_name=validated_data.get('quarto').name
            )
        )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        logger.info(
            'Updating reserva "{reserva_name}" for quarto "{quarto_name}".'.format(
                reserva_name=validated_data.get('name'),
                quarto_name=validated_data.get('quarto').name
            )
        )
        return super().update(instance, validated_data)

    def validate(self, data):
        quarto = data.get('quarto')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        status = data.get('status')
        reserva_id = self.context.get('request').data.get('id')

        if start_date and end_date:
            if start_date > end_date:
                logger.error(
                    'Problem trying to validate meeting. Start cannot be greater than end.',
                )
                raise serializers.ValidationError('Start cannot be greater than end.')
            if quarto.conflict(
                start_date=start_date,
                end_date=end_date,
                reserva_id=reserva_id,
            ) and status == 'scheduled':
                logger.error(
                    'Problem trying to validate reserva. Quarto {quarto} already booked in this period.'.format(
                        quarto=quarto.name,
                    )
                )
                raise serializers.ValidationError(
                    'Quarto {quarto} already booked in this period.'.format(
                        quarto=quarto.name
                    )
                )
        return data
