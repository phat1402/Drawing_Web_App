import random
import re

import requests
from django.core.cache import cache
from django.db.models import Count, Max, Avg, F, IntegerField, Sum, Case, When
from django.views import generic
from django.views.generic.base import ContextMixin
from api.models import UserInfor, Photolike, Photo, Followed, Comment
from django.shortcuts import get_object_or_404
from django.db.models import Q


class HomePage(generic.TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return super(HomePage,self).get(request, *args, **kwargs)

class MyGallery(generic.TemplateView):
    template_name = 'mygallery.html'

    def get(self, request, *args, **kwargs):
        print(request.session.get('username'))
        photos = Photo.objects.filter(username=request.session.get('username'))
        number_of_photos = photos.count()
        kwargs['photos'] = photos
        kwargs['username'] = request.session.get('username')
        kwargs['numberofphoto'] = number_of_photos
        return super(MyGallery, self).get(request, *args, **kwargs)

class FriendGallery(generic.TemplateView):
    template_name = 'friend_gallery.html'

    def get(self, request, *args, **kwargs):
        photos = Photo.objects.filter(username=kwargs['username'])
        number_of_photos = photos.count()
        kwargs['photos'] = photos
        kwargs['numberofphoto'] = number_of_photos
        return super(FriendGallery, self).get(request, *args, **kwargs)

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
        kwargs['photo_link_db'] = photo.photo_link
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

class GalleryImageDetail(generic.TemplateView):
    template_name = 'image_detail_gallery.html'

    def get(self, request, *args, **kwargs):
        photo = get_object_or_404(Photo, photo_id = kwargs['photo_id'])
        kwargs['photo_link_db'] = photo.photo_link
        kwargs['photo_title'] = photo.photo_name
        kwargs['username'] = photo.username.username
        photo_id = photo.pk
        kwargs['photo_link_db'] = photo.photo_link
        print(photo_id)
        # filter_args_comment = {'username': request.session.get('username'), 'photo_id': photo_id }
        comment_obj = Comment.objects.filter(username=request.session.get('username'), photo__photo_id=photo_id)
        kwargs['comments'] = comment_obj
        kwargs['user_has_commented'] = request.session.get('username')
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

        return super(GalleryImageDetail, self).get(request, *args, **kwargs)

class EditImage(generic.TemplateView):
    template_name = 'edit_image.html'

    def get(self, request, *args, **kwargs):
        photo = get_object_or_404(Photo, photo_id = kwargs['photo_id'])
        kwargs['photo_link_db'] = photo.photo_link
        kwargs['photo_name_db'] = photo.photo_name
        kwargs['photo_id'] = photo.pk
        return super(EditImage, self).get(request, *args, **kwargs)

class NewsFeed(generic.TemplateView):
    template_name = 'newsfeed.html'

    def get(self, request, *args, **kwargs):
        username = request.session.get('username')
        followeds = Followed.objects.filter(username=username)
        photo_list = []
        photo_list_explore = []
        username_array =[]
        for user_follow in followeds:
            username_follow = user_follow.followed
            photos = Photo.objects.filter(username=username_follow)
            for photo in photos:
                photo_list.append(photo)
            username_array.append(username_follow)
        username_array.append(username)
        user_not_follow = UserInfor.objects.exclude(username__in = username_array)
        for user in user_not_follow:
            username_not_follow = user.username
            photos = Photo.objects.filter(username=username_not_follow)
            for photo in photos:
                photo_list_explore.append(photo)
        kwargs['photo_list'] = photo_list
        kwargs['photo_list_explore'] = photo_list_explore
        return super(NewsFeed, self).get(request, *args, **kwargs)

class FriendImageDetail(generic.TemplateView):
    template_name = 'newsfeed_image.html'

    def get(self, request, *args, **kwargs):
        return super(FriendImageDetail, self).get(request, *args, **kwargs)

class UserGallery(generic.TemplateView):
    template_name = 'usergallery.html'
    def get(self, request, *args, **kwargs):
        return super(UserGallery, self).get(request, *args, **kwargs)

class PageNotFound(generic.TemplateView):
    template_name = '404.html'
    def get(self, request, *args, **kwargs):
        return super(PageNotFound, self).get(request, *args, **kwargs)