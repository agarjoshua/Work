# Generated by Django 3.1.7 on 2022-10-03 07:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=350)),
                ('description', models.CharField(max_length=450)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=350)),
                ('image', models.ImageField(upload_to='')),
                ('category', models.CharField(max_length=220)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servicemanager.author')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=350)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='Not applicable', max_length=220)),
                ('details', models.CharField(default='Not applicable', max_length=220)),
                ('pages', models.CharField(default='Not applicable', max_length=220)),
                ('file', models.FileField(default='Not applicable', upload_to='')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('issued', models.BooleanField(default=False)),
                ('issued_at', models.DateTimeField(blank=True, null=True)),
                ('Department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.department')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('issued', models.BooleanField(default=False)),
                ('issued_at', models.DateTimeField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servicemanager.book')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.employee')),
            ],
        ),
    ]