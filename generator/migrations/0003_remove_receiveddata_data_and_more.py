# Generated by Django 4.2.11 on 2024-04-16 08:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0002_receiveddata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receiveddata',
            name='data',
        ),
        migrations.RemoveField(
            model_name='receiveddata',
            name='received_at',
        ),
        migrations.AddField(
            model_name='receiveddata',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='receiveddata',
            name='key',
            field=models.CharField(default='default_key', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='receiveddata',
            name='value',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
