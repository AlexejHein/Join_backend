# Generated by Django 4.2.11 on 2024-04-16 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReceivedData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField()),
                ('received_at', models.DateTimeField(auto_now_add=True)),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generator.token')),
            ],
        ),
    ]
