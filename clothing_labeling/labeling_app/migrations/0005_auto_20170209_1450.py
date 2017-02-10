# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-02-09 14:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('labeling_app', '0004_usercurrentimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='userspecifics',
            name='usr_finished',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='boundingbox',
            name='bbx_img_cat_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bounding_box', to='labeling_app.ImageCategories'),
        ),
    ]
