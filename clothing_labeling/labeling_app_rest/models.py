from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    img_id = models.AutoField(primary_key=True)
    img_location = models.CharField(blank=False, max_length=200)

class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_description = models.CharField(blank=False, max_length=50)
    cat_main = models.BooleanField(default=False)

class BoundingBox(models.Model):
    bbx_id = models.AutoField(primary_key=True)
    bbx_img_cat_id = models.ForeignKey('ImageCategories', on_delete=models.CASCADE, related_name='image_category')
    bbx_x = models.FloatField(default=0.0)
    bbx_y = models.FloatField(default=0.0)
    bbx_height = models.FloatField(default=0.0)
    bbx_width = models.FloatField(default=0.0)
    bbx_reviewed = models.BooleanField(default=False)
    bbx_verified = models.BooleanField(default=False)

class ImageCategories(models.Model):
    ict_id = models.AutoField(primary_key=True)
    ict_img = models.ForeignKey('Image', on_delete=models.CASCADE, related_name='image')
    ict_cat = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='categories')
    ict_added_bb = models.BooleanField(default=False)
    ict_valid = models.BooleanField(default=True)
    ict_taken_for_labeling = models.BooleanField(default=False)

