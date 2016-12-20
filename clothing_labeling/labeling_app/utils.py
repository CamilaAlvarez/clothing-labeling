from labeling_app.models import ImageCategories, BoundingBox, Image
from labeling_app.serializers import ImageCategoriesSerializer, BoundingBoxSerializer

def no_results_left():
    final_image = Image.objects.get(pk=0)
    return {"image": {"image": 0, "image_url": final_image.img_location},
            "end": True}

def obtain_unlabeled_image():
    try:
        image_categories = ImageCategories.objects.filter(ict_added_bb=False)
    except ImageCategories.DoesNotExist:
        return no_results_left()
    if len(image_categories) == 0:
        return no_results_left()
    next_image = image_categories[0]
    image_serializer = ImageCategoriesSerializer(next_image, many=False)
    return image_serializer.data


def obtain_unreviewed_bb():
    try:
        bounding_boxes = BoundingBox.objects.filter(bbx_reviewed=False)
    except BoundingBox.DoesNotExist:
        return no_results_left()
    if len(bounding_boxes)==0:
        return no_results_left()
    next_bounding_box = bounding_boxes[0]
    bounding_box_serializer = BoundingBoxSerializer(next_bounding_box, many=False)
    return bounding_box_serializer.data

