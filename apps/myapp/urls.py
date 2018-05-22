from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^my_page$', views.my_page),
    url(r'^logout$', views.logout),
    url(r'^add_trip$', views.add_trip),
    url(r'^show_trip/(?P<trip_id>\d+)$', views.show_trip),
    url(r'^join/(?P<trip_id>\d+)$', views.join),
    url(r'^create_trip$', views.create_trip),
    # url(r'^home$', views.index)

]
