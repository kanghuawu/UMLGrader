from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^loginredirect/$', views.loginredirect, name='loginredirect'),
    url(r'^(?P<username>[\w.@+-]+)/$', views.grader, name='grader'),
    url(r'^$', views.grader, name='grader'),
]