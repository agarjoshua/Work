# Generated by Django 3.1.7 on 2022-12-01 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicemanager', '0010_auto_20221201_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docservice',
            name='department',
            field=models.CharField(max_length=350),
        ),
    ]
