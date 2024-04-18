# Generated by Django 4.2.11 on 2024-04-16 14:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0006_storageitem_delete_receiveddata'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReceivedData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('value', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('version', models.IntegerField(default=1)),
            ],
        ),
        migrations.AddField(
            model_name='token',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='StorageItem',
        ),
        migrations.AddField(
            model_name='receiveddata',
            name='token',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generator.token'),
        ),
    ]