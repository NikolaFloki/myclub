# Generated by Django 4.0 on 2022-10-31 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_event_manager'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myclubuser',
            old_name='emai',
            new_name='email',
        ),
    ]
