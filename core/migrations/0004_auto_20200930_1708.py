# Generated by Django 3.1.1 on 2020-09-30 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200930_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='comprovante',
            field=models.FileField(blank=True, null=True, upload_to='media/reserva'),
        ),
    ]
