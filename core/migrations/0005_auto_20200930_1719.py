# Generated by Django 3.1.1 on 2020-09-30 20:19

from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200930_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='comprovante',
            field=stdimage.models.StdImageField(blank=True, null=True, upload_to='reserva'),
        ),
    ]
