from django.conf.urls import url

from . import views, forms

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^detail/$', views.detailIndex, name='detail index'),
	url(r'^detail/(?P<room_rating_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^create/$', views.create, name='create'),
	url(r'^auth/$', views.login, name='login'),
	#url(r'^create/new/$', forms.create, name='create_new'),
]