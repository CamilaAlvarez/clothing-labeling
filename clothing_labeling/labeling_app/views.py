from django.shortcuts import render

#Pages
def index(request):
    return render(request, 'labeling_app/basic-labeling.html', {'controller': 'DrawerController',
                                                                'controller_short': 'drawer',
                                                                'app': "Labeling",
                                                                "request_controller": "BasicLabelingController"})

def verifier(request):
    return render(request, 'labeling_app/verifier.html', {'request_controller': 'MainController',
                                                           'app': 'Verifier',
                                                            'controller': 'BoundingBoxController',
                                                            'controller_short': 'bbx'
                                                          })

def transformer(request):
    return render(request, 'labeling_app/category-labeling.html', {'controller': 'DrawerController',
                                                                    'controller_short': 'drawer',
                                                                    'app': "Labeling",
                                                                    "request_controller": "CategoryLabelingController"
                                                                   })


