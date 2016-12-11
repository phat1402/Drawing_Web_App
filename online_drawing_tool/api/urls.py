from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^send_login$', views.SendLoginAPI.as_view()),
    url(r'^send_register$', views.SendRegisterAPI.as_view()),

    #url(r'^autocomplete_search$',views.autocomplete_search, name= 'autocomplete_search'),
    #url(r'^autocompleteModel$',views.autocompleteModel, name= 'autocompleteModel'),
    url(r'^search$',  views.search_titles,   name="ajax_search_view"),
    url(r'^follow$', views.followstatus),
    url(r'^follow_action$',views.follow),
    url(r'^logout$', views.log_out),
    url(r'^getfollower$',views.getFollower),
    url(r'^getfollowing$',views.getFollowing),
    # url(r'^saveimage',views.saveimage),

]
