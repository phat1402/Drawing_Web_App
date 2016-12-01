from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^send_login$', views.SendLoginAPI.as_view()),
    url(r'^send_register$', views.SendRegisterAPI.as_view()),
]
