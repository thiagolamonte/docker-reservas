# Generated by Django 3.1.1 on 2020-09-30 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200930_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='comprovante',
            field=models.FileField(blank=True, null=True, upload_to='reserva'),
        ),
    ]
