from django.conf.urls import url
import labeling_app_rest.views as views

urlpatterns = [
    url(r'next-image$', views.get_next_image, name='next-image'),
    url(r'write-bounding-box$', views.write_bounding_box, name='write-bb'),
    url(r'next-label$', views.next_label, name='next-label'),
    url(r'verify-label$', views.review_label, name='verify-label'),
    url(r'categories$', views.get_categories, name='categories'),
    url(r'write-category-bounding-box$', views.write_bounding_box_with_category, name='write-bb-category'),
    url(r'next-image-invalid-category$', views.get_next_image_invalid_category, name='next-image-category'),
]