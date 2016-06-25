from django.conf.urls import url

from . import views

app_name = 'emails'
urlpatterns = [
    url(r'^$', views.subscribe, name='subscribe'),
]
