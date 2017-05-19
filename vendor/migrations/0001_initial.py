# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-15 01:32
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.CharField(default='', max_length=15)),
                ('lng', models.CharField(default='', max_length=15)),
                ('temperature', models.FloatField(null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(default='', max_length=50)),
                ('ip', models.GenericIPAddressField(null=True, protocol='IPv4')),
                ('seller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='machines', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Popsicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flavor', models.CharField(max_length=50, unique=True)),
                ('price', models.CharField(default='100', max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='PopsicleEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.Machine')),
                ('popsicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.Popsicle')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PopsicleRemoval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.Machine')),
                ('popsicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.Popsicle')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('lid_was_released', models.BooleanField(default=False)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.Machine')),
                ('popsicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.Popsicle')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(default=0)),
                ('updated_at', models.DateField(auto_now=True)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='vendor.Machine')),
                ('popsicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.Popsicle')),
            ],
        ),
        migrations.AddField(
            model_name='location',
            name='machine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='vendor.Machine'),
        ),
    ]
