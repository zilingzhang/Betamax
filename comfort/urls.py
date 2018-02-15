from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^detail/$', views.detailIndex, name='detail index'),
	url(r'^detail/(?P<room_rating_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^create/$', views.create, name='create'),
]