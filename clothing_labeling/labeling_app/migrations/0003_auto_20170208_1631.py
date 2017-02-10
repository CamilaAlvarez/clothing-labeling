# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-02-08 16:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('labeling_app', '0002_auto_20170208_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='cat_descriptive_image',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='userimages',
            name='uim_image_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='labeling_app.ImageCategories'),
        ),
        migrations.AlterField(
            model_name='userimages',
            name='uim_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_images', to=settings.AUTH_USER_MODEL),
        ),
    ]
