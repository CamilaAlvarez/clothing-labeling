from labeling_app_rest.models import ImageCategories, BoundingBox, Image, Category
from labeling_app_rest.serializers import ImageCategoriesSerializer, BoundingBoxSerializer, CategorySerializer

import logging

logger = logging.getLogger("clothing_labeling")


def no_results_left():
    final_image = Image.objects.get(img_id=1) #mysql doesn't support 0 as autovalue field
    return {"image": {"image": 1, "image_url": final_image.img_location},
            "end": True}

def obtain_unlabeled_image():
    try:
        next_image = ImageCategories.objects.filter(ict_added_bb=False, ict_cat__cat_main__exact=True,
                                                          ict_valid= True, ict_taken_for_labeling=False)[0]
    except (ImageCategories.DoesNotExist, IndexError):
        return no_results_left()
    if next_image is None:
        return no_results_left()

    image_serializer = ImageCategoriesSerializer(next_image, many=False)
    next_image.ict_taken_for_labeling = True
    next_image.save()
    return image_serializer.data


def obtain_unlabeled_image_invalid_category():
    try:
        next_image = ImageCategories.objects.filter(ict_added_bb=False, ict_cat__cat_main__exact=False,
                                                          ict_valid=True)[0]
    except (ImageCategories.DoesNotExist, IndexError):
        return no_results_left()
    if next_image is None:
        return no_results_left()
    image_serializer = ImageCategoriesSerializer(next_image, many=False)
    return image_serializer.data

def obtain_unreviewed_bb():
    try:
        next_bounding_box = BoundingBox.objects.filter(bbx_reviewed=False,
                                                       bbx_img_cat_id__ict_cat__cat_main__exact=True)[0]
    except (BoundingBox.DoesNotExist, IndexError):
        return no_results_left()
    if next_bounding_box is None:
        return no_results_left()
    bounding_box_serializer = BoundingBoxSerializer(next_bounding_box, many=False)
    return bounding_box_serializer.data


def get_all_categories():
    categories = Category.objects.filter(cat_main=True)
    category_serializer = CategorySerializer(categories, many=True)
    return category_serializer.data


def obtain_bb_invalid_category():
    bounding_box = BoundingBox.objects.filter(bbx_img_cat_id__ict_cat__cat_main__exact=False)
    if len(bounding_box) > 0:
        bb = bounding_box[0]
        bb.bbx_verified = 0
        bb.bbx_reviewed = 0
        bb.save()
        bounding_box_serializer = BoundingBoxSerializer(bb)
        return bounding_box_serializer.data
    else:
        return no_results_left()

