from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
  url(r'^(?P<lang>[a-z]{2})/page/cat/$', views.objIndex, name='oindex'),
  url(r'^(?P<lang>[a-z]{2})/page/cat/(?P<code>[A-Za-z0-9]+)/$', views.objView, name='oview'),
  url(r'^(?P<lang>[a-z]{2})/page/(?P<slug>[A-Za-z0-9_-]+)/$', views.pageView, name='pview'),
  url(r'^(?P<lang>[a-z]{2})/bpage/(?P<slug>[A-Za-z0-9_-]+)/$', views.briefView, name='bview'),
  url(r'^$',RedirectView.as_view(url='/ru/page/home/',permanent=True)),  
]