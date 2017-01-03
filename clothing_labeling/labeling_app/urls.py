from labeling_app import views
from django.conf.urls import url

urlpatterns = [
    url(r'^verifier[$/]', views.verifier, name='verifier'),
    url(r'^transform-categories[$/]', views.transformer, name = 'transformer'),
    url(r'^assign-category-to-bbox[$/]', views.transform_category, name='transformer'),
    url(r'^home[$/]', views.index, name='index'),
    url(r'^$', views.index, name='other-index')

]