from django.conf.urls import url
from django.contrib.auth import views as auth_views

from image_to_link import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.upload_file, name = 'upload_file'),
    url(r'^$', auth_views.login, {'template_name': 'image_to_link/login.html'}, name='login'),
    # url(r'^$', views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'image_to_link/logout.html'}, name='logout'),
    #url(r'^process_image/$', views.process_image, name = 'process_image'),
    #url(r'^upload/$', views.upload_file, name = 'upload_file'),
]
