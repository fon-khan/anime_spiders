# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-16 18:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibition', '0006_add_anime_episodes_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='cg',
            name='path',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
