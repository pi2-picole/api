# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-07 15:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_auto_20170617_1329'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.FloatField(null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temperatures', to='vendor.Machine')),
            ],
        ),
        migrations.RemoveField(
            model_name='location',
            name='temperature',
        ),
    ]