# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-02-10 16:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labeling_app', '0005_auto_20170209_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagecategories',
            name='ict_is_test',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userspecifics',
            name='usr_blocked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userspecifics',
            name='usr_comitted_fraude',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userspecifics',
            name='usr_has_show_fraude_info',
            field=models.BooleanField(default=True),
        ),
    ]
