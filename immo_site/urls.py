from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
  url(r'^(?P<lang>[a-z]{2})/page/cat/$', views.objIndex, name='oindex'),
  url(r'^(?P<lang>[a-z]{2})/page/cat/(?P<code>[A-Za-z0-9]+)/$', views.objView, name='oview'),
  url(r'^(?P<lang>[a-z]{2})/page/(?P<slug>[A-Za-z0-9_-]+)/$', views.pageView, name='pview'),
  url(r'^(?P<lang>[a-z]{2})/bpage/(?P<slug>[A-Za-z0-9_-]+)/$', views.briefView, name='bview'),
  url(r'^(?P<lang>[a-z]{2})/qpage/(?P<slug>[A-Za-z0-9_-]+)/$', views.questView, name='qview'),
  url(r'^(?P<lang>[a-z]{2})/qpage/(?P<slug>[A-Za-z0-9_-]+)/ans/1307(?P<ans>[0-9]+)/$', views.questView, name='qview'),
  url(r'^$',RedirectView.as_view(url='/ru/page/home/',permanent=True)),  
]