from labeling_app_rest.models import ImageCategories, BoundingBox, Image, Category
from labeling_app_rest.serializers import ImageCategoriesSerializer, BoundingBoxSerializer, CategorySerializer


def no_results_left():
    final_image = Image.objects.get(pk=1) #mysql doesn't support 0 as autovalue field
    return {"image": {"image": 1, "image_url": final_image.img_location},
            "end": True}

def obtain_unlabeled_image():
    try:
        image_categories = ImageCategories.objects.filter(ict_added_bb=False, ict_cat__cat_main__exact=True)
    except ImageCategories.DoesNotExist:
        return no_results_left()
    if len(image_categories) == 0:
        return no_results_left()
    next_image = image_categories[0]
    image_serializer = ImageCategoriesSerializer(next_image, many=False)
    return image_serializer.data


def obtain_unlabeled_image_invalid_category():
    try:
        image_categories = ImageCategories.objects.filter(ict_added_bb=False, ict_cat__cat_main__exact=False)
    except ImageCategories.DoesNotExist:
        return no_results_left()
    if len(image_categories) == 0:
        return no_results_left()
    next_image = image_categories[0]
    image_serializer = ImageCategoriesSerializer(next_image, many=False)
    return image_serializer.data

def obtain_unreviewed_bb():
    try:
        bounding_boxes = BoundingBox.objects.filter(bbx_reviewed=False, bbx_img_cat_id__ict_cat__cat_main__exact=True)
    except BoundingBox.DoesNotExist:
        return no_results_left()
    if len(bounding_boxes)==0:
        return no_results_left()
    next_bounding_box = bounding_boxes[0]
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