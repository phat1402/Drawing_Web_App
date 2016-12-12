import random
import re

import requests
from django.core.cache import cache
from django.db.models import Count, Max, Avg, F, IntegerField, Sum, Case, When
from django.views import generic
from django.views.generic.base import ContextMixin
from api.models import UserInfor, Photolike, Photo, Comment
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
        photo_id = photo.pk
        kwargs['photo_link_db'] = photo.photo_link
        print(photo_id)
        filter_args_comment = {'photo_id': photo_id, 'username': request.session.get('username')}
        comment_objs = Comment.objects.filter(**filter_args_comment)
        print (comment_objs)
        kwargs['comments'] = comment_objs
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
        return super(NewsFeed, self).get(request, *args, **kwargs)

class FriendImageDetail(generic.TemplateView):
    template_name = 'newsfeed_image.html'

    def get(self, request, *args, **kwargs):
        return super(FriendImageDetail, self).get(request, *args, **kwargs)