from django.conf.urls import url

from image_to_link import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.upload_file, name = 'upload_file'),
    #url(r'^process_image/$', views.process_image, name = 'process_image'),
    #url(r'^upload/$', views.upload_file, name = 'upload_file'),
]
