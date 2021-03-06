from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^send_login$', views.SendLoginAPI.as_view()),
    url(r'^send_register$', views.SendRegisterAPI.as_view()),

    #url(r'^autocomplete_search$',views.autocomplete_search, name= 'autocomplete_search'),
    #url(r'^autocompleteModel$',views.autocompleteModel, name= 'autocompleteModel'),
    url(r'^search$',  views.search_titles, name="ajax_search_view"),
    url(r'^logout$', views.log_out),
    url(r'^like_blog$', views.like_ajax, name='like'),
    url(r'^saveimage$',views.saveimage),
    url(r'^resetForm$', views.ResetPasswordRequestView.as_view()),
    url(r'^user_search$' ,views.search_user),
    url(r'^follow$', views.followstatus),
    url(r'^follow_action$',views.follow),
    url(r'^getfollower$',views.getFollower),
    url(r'^getfollowing$',views.getFollowing),
    url(r'^sessfollower$',views.sessFollower),
    url(r'^sessfollowing$',views.sessFollowing),
    url(r'^save_edited_image$',views.save_edited_image),
    url(r'^comment$', views.comment, name='comment'),
    url(r'^deleteimage$',views.deleteimage),
]
