from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from labeling_app_rest.utils import obtain_unlabeled_image, obtain_unreviewed_bb, get_all_categories,obtain_unlabeled_image_invalid_category
from labeling_app_rest.exceptions import InvalidImageCategory
from labeling_app_rest.serializers import BoundingBoxRequestSerializer, VerifiedBoundingBoxSerializer, BoundingBoxWithCategorySerializer


#Services
@api_view(['GET','POST'])
def get_next_image(request):
    response = obtain_unlabeled_image()
    return Response(response, status.HTTP_200_OK)

@api_view(['POST'])
def write_bounding_box(request):
    json_data = JSONParser().parse(request)
    deserialized_data = BoundingBoxRequestSerializer(data=json_data)
    if deserialized_data.is_valid():
        try:
            deserialized_data.save()
        except InvalidImageCategory:
            return Response({'error': 'Invalid request'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        next_image = obtain_unlabeled_image()
        return Response(next_image, status.HTTP_200_OK)
    return Response(deserialized_data.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def next_label(request):
    response = obtain_unreviewed_bb()
    return Response(response, status.HTTP_200_OK)



@api_view(['POST'])
def review_label(request):
    json_data = JSONParser().parse(request)
    deserialized_data = VerifiedBoundingBoxSerializer(data=json_data, many=False)
    if deserialized_data.is_valid():
        try:
            deserialized_data.save()
        except InvalidImageCategory:
            return Response({'error': 'Invalid request'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        next_label = obtain_unreviewed_bb()
        return Response(next_label, status.HTTP_200_OK)
    return Response(deserialized_data.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_categories(request):
    response = get_all_categories()
    return Response(response, status.HTTP_200_OK)


@api_view(['POST'])
def write_bounding_box_with_category(request):
    json_data = JSONParser().parse(request)
    deserialized_data = BoundingBoxWithCategorySerializer(data=json_data)
    if deserialized_data.is_valid():
        try:
            deserialized_data.save()
        except InvalidImageCategory:
            return Response({'error': 'Invalid request'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        next_image = obtain_unlabeled_image_invalid_category()
        return Response(next_image, status.HTTP_200_OK)
    return Response(deserialized_data.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_next_image_invalid_category(request):
    response = obtain_unlabeled_image_invalid_category()
    return Response(response, status.HTTP_200_OK)