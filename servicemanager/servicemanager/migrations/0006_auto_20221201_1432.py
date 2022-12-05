# Generated by Django 3.1.7 on 2022-12-01 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servicemanager', '0005_auto_20221201_1359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='docservice',
            name='book',
        ),
        migrations.RemoveField(
            model_name='docservice',
            name='cost',
        ),
        migrations.AddField(
            model_name='docservice',
            name='service_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='servicemanager.servicetype'),
        ),
    ]