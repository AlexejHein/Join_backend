# Generated by Django 4.2.11 on 2024-04-18 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0008_alter_receiveddata_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='receiveddata',
            unique_together=set(),
        ),
    ]
