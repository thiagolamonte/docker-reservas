from stdimage.models import StdImageField
from django.core.exceptions import ValidationError
from django.db import models


class Quarto(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField()
    endereco = models.CharField(max_length=200, blank=True, null=True)
    tratar = models.CharField(max_length=100, unique=True, null=True)
    telefone = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    imagem = StdImageField(upload_to='quartos', blank=True, null=True, variations={'thumb': {'width': 480, 'height': 480}})
    color = models.CharField(max_length=20, blank=True, null=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.color = self.color.lower() if self.color else ''
        return super().save(*args, **kwargs)

    def conflict(self, start_date, end_date, reserva_id):
        return self.reservas.filter(
            start_date__lt=end_date,
            end_date__gt=start_date,
        ).exclude(
            id=reserva_id
        ).exists()


class Reserva(models.Model):
    SCHEDULED = 'scheduled'
    CANCELED = 'canceled'
    STATUS_CHOICES = (
        (SCHEDULED, 'Scheduled'),
        (CANCELED, 'Canceled'),
    )
    quarto = models.ForeignKey(
        'core.Quarto',
        related_name='reservas',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=SCHEDULED,
        db_index=True
    )
    start_date = models.DateField(db_index=True, blank=True, null=True)
    end_date = models.DateField(db_index=True, blank=True, null=True)
    comprovante = StdImageField(upload_to='reservas', blank=True, null=True,)

    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError('Start cannot be greater than end.')
            if self.quarto.conflict(
                start_date=self.start_date,
                end_date=self.end_date,
                reserva_id=self.id
            ) and self.status == self.SCHEDULED:
                raise ValidationError(
                    'Quarto {quarto} already booked in this period.'.format(
                        quarto=self.quarto.name
                    )
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

