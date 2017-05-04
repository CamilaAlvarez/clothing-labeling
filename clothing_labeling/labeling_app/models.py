from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class UserSpecifics(models.Model):
    usr = models.ForeignKey(User, related_name='specifics')
    usr_has_seen_info = models.BooleanField(default=False)
    usr_times_finished = models.IntegerField(default=0)
    usr_origin = models.CharField(blank=False,max_length=200)
    usr_is_mechanical_turk = models.BooleanField(default=True)
    usr_finished = models.BooleanField(default=False)
    usr_comitted_fraude = models.BooleanField(default=False)
    usr_has_show_fraude_info = models.BooleanField(default=True)
    usr_blocked = models.BooleanField(default=False)


class MechanicalTurkCodes(models.Model):
    mtc_usr = models.ForeignKey(User, related_name='codes')
    mtc_code = models.CharField(blank=False, max_length=200)


class UserCurrentImage(models.Model):
    uci_user = models.ForeignKey(User)
    uci_image_category = models.ForeignKey('ImageCategories')


class UserImages(models.Model):
    uim_user = models.ForeignKey(User, related_name='user_images')
    uim_image_category = models.ForeignKey('ImageCategories', related_name='images')
    uim_evaluated = models.BooleanField(default=False)


class Image(models.Model):
    img_id = models.AutoField(primary_key=True)
    img_location = models.CharField(blank=False, max_length=200)

    @staticmethod
    def last_image():
        #Cambia a 1 por mysql
        return Image.objects.get(img_id=1)



class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_description = models.CharField(blank=False, max_length=50)
    cat_main = models.BooleanField(default=False)
    cat_descriptive_image = models.CharField(blank=True, max_length=200)


class BoundingBox(models.Model):
    bbx_id = models.AutoField(primary_key=True)
    bbx_img_cat_id = models.OneToOneField('ImageCategories', related_name='bounding_box')
    bbx_x = models.FloatField(default=0.0)
    bbx_y = models.FloatField(default=0.0)
    bbx_height = models.FloatField(default=0.0)
    bbx_width = models.FloatField(default=0.0)
    bbx_reviewed = models.BooleanField(default=False)
    bbx_verified = models.BooleanField(default=False)
    bbx_image_height = models.FloatField(default=0.0)
    bbx_image_width = models.FloatField(default=0.0)

class ImageCategories(models.Model):
    ict_id = models.AutoField(primary_key=True)
    ict_img = models.ForeignKey('Image', related_name='image')
    ict_cat = models.ForeignKey('Category', related_name='categories')
    ict_added_bb = models.BooleanField(default=False)
    ict_valid = models.BooleanField(default=True)
    ict_taken_for_labeling = models.BooleanField(default=False)
    ict_is_test = models.BooleanField(default=False)
