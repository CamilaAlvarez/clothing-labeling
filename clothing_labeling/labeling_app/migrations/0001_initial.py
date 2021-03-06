# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-02-07 22:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('ict_valid', models.BooleanField(default=True)),
                ('ict_taken_for_labeling', models.BooleanField(default=False)),
                ('ict_cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='labeling_app.Category')),
                ('ict_img', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='labeling_app.Image')),
            ],
        ),
        migrations.CreateModel(
            name='UserSpecifics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usr_has_seen_info', models.BooleanField(default=False)),
                ('usr_times_finished', models.IntegerField(default=0)),
                ('usr_origin', models.CharField(max_length=200)),
                ('usr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='boundingbox',
            name='bbx_img_cat_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_category', to='labeling_app.ImageCategories'),
        ),
    ]
