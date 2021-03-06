# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-21 15:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BoundingBox',
            fields=[
                ('bbx_id', models.AutoField(primary_key=True, serialize=False)),
                ('bbx_x', models.FloatField(default=0.0)),
                ('bbx_y', models.FloatField(default=0.0)),
                ('bbx_height', models.FloatField(default=0.0)),
                ('bbx_width', models.FloatField(default=0.0)),
                ('bbx_reviewed', models.BooleanField(default=False)),
                ('bbx_verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('cat_id', models.AutoField(primary_key=True, serialize=False)),
                ('cat_description', models.CharField(max_length=50)),
                ('cat_main', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('img_id', models.AutoField(primary_key=True, serialize=False)),
                ('img_location', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ImageCategories',
            fields=[
                ('ict_id', models.AutoField(primary_key=True, serialize=False)),
                ('ict_added_bb', models.BooleanField(default=False)),
                ('ict_cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='labeling_app_rest.Category')),
                ('ict_img', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='labeling_app_rest.Image')),
            ],
        ),
        migrations.AddField(
            model_name='boundingbox',
            name='bbx_img_cat_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_category', to='labeling_app_rest.ImageCategories'),
        ),
    ]
