# Generated by Django 4.1.4 on 2023-01-02 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_rename_date_event_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatar.png', upload_to=''),
        ),
    ]