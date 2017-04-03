from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name="login"),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login/'}, name="logout"),
    url(r'^password-reset/$', auth_views.password_reset,{'template_name': 'registration/password-reset-form.html',
                                                        },
        name='password-reset'),
    url(r'^password-reset/done/$', auth_views.password_reset_done,
        {'template_name': 'registration/password-reset-done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,{'template_name': 'registration/password-reset-confirm.html'}
        , name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        {'template_name': 'registration/password-reset-complete.html'}, name='password_reset_complete'),
    url(r'^$', auth_views.login, {'template_name': 'registration/login.html'}, name="login"),
]