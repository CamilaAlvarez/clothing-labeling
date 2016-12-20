from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from labeling_app.utils import obtain_unlabeled_image, obtain_unreviewed_bb
from labeling_app.exceptions import InvalidImageCategory
from labeling_app.serializers import BoundingBoxRequestSerializer, VerifiedBoundingBoxSerializer
from django.views.decorators.csrf import csrf_exempt

#Pages
def index(request):
    return render(request, 'labeling_app/basic-labeling.html', {'controller': 'DrawerController',
                                                                'controller_short': 'drawer',
                                                                'app': "Labeling",
                                                                "request_controller": "CanvasController"})

def verifier(request):
    return render(request, 'labeling_app/verifier.html', {'request_controller': 'MainController',
                                                           'app': 'Verifier',
                                                            'controller': 'BoundingBoxController',
                                                            'controller_short': 'bbx'
                                                          })


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

