from labeling_app import views
from labeling_app import registration
from django.conf.urls import url, include

urlpatterns = [
    url(r'^blocked/', views.blocked_user, name="blocked"),
    url(r'^invalidate/', views.invalidate_image, name='invalidate_image'),
    url(r'^add-bbox/', views.evaluate, name='evaluate_image'),
    url(r'^end/', views.end, name='end'),
    url(r'^nothing-left/', views.no_images_left, name='final'),
    url(r'^instructions/', views.get_instructions, name='instructions'),
    url(r'^codes/', views.get_codes, name='codes'),
    url(r'^verify/', registration.verify, name='verify'),
    url(r'^register/$', registration.register, name='register'),
    url(r'^verifier[$/]', views.verifier, name='verifier'),
    url(r'^transform-categories[$/]', views.transformer, name = 'transformer'),
    url(r'^assign-category-to-bbox[$/]', views.transform_category, name='transformer'),
    url(r'^home[$/]', views.index, name='index'),
    url(r'^', include('labeling_app.url_registration'))

]