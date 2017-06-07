from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    url(r'^loginredirect/$', views.loginredirect, name='loginredirect'),
    url(r'^(?P<username>[\w.@+-]+)/$', views.grader, name='grader'),
    url(r'^$', views.grader, name='grader'),
]
