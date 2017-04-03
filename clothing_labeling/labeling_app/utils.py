from .models import UserSpecifics, UserImages, ImageCategories
from .exceptions import NoImagesLeft, BlockedUser
import random
import math


def set_has_seen_info(user):
    user_specifics = UserSpecifics.objects.get(usr=user)
    if not user_specifics.usr_has_seen_info:
        user_specifics.usr_has_seen_info = True
        user_specifics.save()


def get_images_user(user):
    images = ImageCategories.objects.raw("SELECT * FROM labeling_app_imagecategories "
                                         "JOIN labeling_app_category ON ict_cat_id=cat_id "
                                         "WHERE ict_added_bb=0 AND ict_is_test=0 AND ict_valid=1 AND "
                                         "ict_id NOT IN (SELECT uim_image_category_id FROM labeling_app_userimages)"
                                         " AND cat_main=1 ORDER BY ict_id")

    if len(list(images)) == 0:
        raise NoImagesLeft
    user_images_categories = images[:10]
    if len(user_images_categories) == 0:
        return []
    images = ImageCategories.objects.filter(ict_is_test=True).order_by('ict_id')

    shuffled = sorted(images, key=lambda x: random.random())
    user_images_categories_list = list(user_images_categories)
    if len(shuffled) > 0:
        user_images_categories_list.append(shuffled[0])
    random.shuffle(user_images_categories_list)
    for image in user_images_categories_list:
        user_image = UserImages(uim_user=user, uim_image_category=image)
        user_image.save()
    user_images = UserImages.objects.filter(uim_user=user, uim_image_category__ict_added_bb=False,
                                            uim_image_category__ict_valid=True)
    return user_images


def set_user_commited_fraud(user):
    user_specifics = UserSpecifics.objects.get(usr=user)
    if user_specifics.usr_comitted_fraude:
        user_specifics.usr_blocked = True
        user_specifics.save()
        raise BlockedUser
    user_specifics.usr_has_show_fraude_info = False
    user_specifics.usr_comitted_fraude = True
    user_specifics.save()


def is_valid_bbox(image, x, y, width, height):
    bbox = image.bounding_box
    test_range_x = set(range(int(math.floor(bbox.bbx_x)), int(math.floor(bbox.bbx_width))+1))
    test_range_y = set(range(int(math.floor(bbox.bbx_y)), int(math.floor(bbox.bbx_height)) + 1))
    bbox_range_x = set(range(int(math.floor(float(x))), int(math.floor(float(width))) + 1))
    bbox_range_y = set(range(int(math.floor(float(y))), int(math.floor(float(height))) + 1))
    return len(test_range_x.intersection(bbox_range_x)) != 0 and len(test_range_y.intersection(bbox_range_y)) != 0



def check_end(user):
    user_images = UserImages.objects.filter(uim_evaluated=False, uim_user=user)
    return len(user_images) != 0