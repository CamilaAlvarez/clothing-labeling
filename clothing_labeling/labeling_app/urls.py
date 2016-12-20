from labeling_app import views
from django.conf.urls import url

urlpatterns = [
    url(r'^api/rest/next-image$', views.get_next_image, name='next-image'),
    url(r'^api/rest/write-bounding-box$', views.write_bounding_box, name='write-bb'),
    url(r'^api/rest/next-label$', views.next_label, name='next-label'),
    url(r'^api/rest/verify-label$', views.review_label, name='verify-label'),
    url(r'^home', views.index, name='index'),
    url(r'^verifier', views.verifier, name='verifier')

]