"""onlinedrawingtool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
import api.urls
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.HomePage.as_view(), name='HomePage'),
    url(r'^landing$', views.HomePage.as_view(), name='LandingPage'),
    url(r'^mygallery', views.MyGallery.as_view(), name='MyGallery'),
    url(r'^image_detail(?P<photo_id>[\w-]+)$', views.ImageDetail.as_view(), name='ImageDetail'),
    url(r'^stranger_detail(?P<photo_id>[\w-]+)$', views.ImageDetailStranger.as_view(), name='ImageDetailStranger'),
    url(r'^gallery_item(?P<photo_id>[\w-]+)$', views.GalleryImageDetail.as_view(), name='GalleryImageDetail'),
    url(r'^edit_image(?P<photo_id>[\w-]+)$', views.EditImage.as_view(), name='EditImage'),
    url(r'^friend_gallery(?P<username>[\w-]+)$', views.FriendGallery.as_view(), name='FriendGallery'),
    url(r'^stranger_gallery(?P<username>[\w-]+)$', views.StrangerGallery.as_view(), name='StrangerGallery'),
    url(r'^coloringpage', views.ColoringPage.as_view(), name='ColoringPage'),
    url(r'^newsfeed', views.NewsFeed.as_view(), name='NewsFeed'),
    url(r'^friend_image_detail', views.FriendImageDetail.as_view(), name='FriendImageDetail'),
    url(r'^upload', views.upload_image, name="upload_image"),
    url(r'^api/', include(api.urls, namespace='api')),
    url(r'^usergallery',views.UserGallery.as_view(),name='UserGallery'),
    url(r'^pagenotfound',views.PageNotFound.as_view(),name='PageNotFound')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


