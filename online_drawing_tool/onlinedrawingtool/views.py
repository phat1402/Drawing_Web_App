import random
import re

import requests
from django.core.cache import cache
from django.db.models import Count, Max, Avg, F, IntegerField, Sum, Case, When
from django.views import generic
from django.views.generic.base import ContextMixin
from api.models import UserInfor, Photolike, Photo, Followed
from django.shortcuts import get_object_or_404


class HomePage(generic.TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return super(HomePage,self).get(request, *args, **kwargs)

class MyGallery(generic.TemplateView):
    template_name = 'mygallery.html'

    def get(self, request, *args, **kwargs):
        print(request.session.get('username'))
        photos = Photo.objects.filter(username=request.session.get('username'))
        kwargs['photos'] = photos
        kwargs['username'] = request.session.get('username')
        return super(MyGallery, self).get(request, *args, **kwargs)

class ColoringPage(generic.TemplateView):
    template_name = 'coloringpage.html'

    def get(self, request, *args, **kwargs):
        return super(ColoringPage,self).get(request, *args, **kwargs)


class ImageDetail(generic.TemplateView):
    template_name = 'image_detail.html'

    def get(self, request, *args, **kwargs):
        photo = get_object_or_404(Photo, photo_id = kwargs['photo_id'])
        kwargs['photo_link_db'] = photo.photo_link
        kwargs['photo_title'] = photo.photo_name
        kwargs['username'] = photo.username.username
        photo_id = photo.pk
        print(photo_id)
        photo_liked = Photolike.objects.filter(photo__photo_id=photo_id)
        try:
            user_liked = photo_liked.get(username=request.session.get('username'))


        except Photolike.DoesNotExist:
            user_liked = None
        if user_liked is None:
            liked = False
            # request.session['has_liked_' + str(photo_id)] = liked
        else:
            liked = True

        kwargs['post'] = photo_id
        kwargs['liked'] = liked
        kwargs['num_likes'] = Photolike.objects.filter(photo__photo_id=photo_id).count()

        return super(ImageDetail, self).get(request, *args, **kwargs)

class NewsFeed(generic.TemplateView):
    template_name = 'newsfeed.html'

    def get(self, request, *args, **kwargs):
        username = request.session.get('username')
        followeds = Followed.objects.filter(username= username)
        photo_list = []
        for user_follow in followeds:
            username_follow = user_follow.followed
            photos = Photo.objects.filter(username=username_follow )
            for photo in photos:
                photo_list.append(photo)

        kwargs['photo_list'] = photo_list
        return super(NewsFeed, self).get(request, *args, **kwargs)

class FriendImageDetail(generic.TemplateView):
    template_name = 'newsfeed_image.html'

    def get(self, request, *args, **kwargs):
        return super(FriendImageDetail, self).get(request, *args, **kwargs)