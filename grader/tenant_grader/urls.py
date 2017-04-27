from django.conf.urls import url

from . import views

app_name = 'grader'
urlpatterns = [
    url(r'^$', views.grader, name='grader'),
]