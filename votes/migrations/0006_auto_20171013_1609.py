# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-13 16:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0005_auto_20170414_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='election',
            name='open',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
