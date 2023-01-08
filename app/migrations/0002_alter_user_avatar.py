# Generated by Django 4.1.4 on 2023-01-07 23:59

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=django_resized.forms.ResizedImageField(crop=None, default='avatar.png', force_format=None, keep_meta=True, quality=-1, scale=None, size=[300, 300], upload_to=''),
        ),
    ]
