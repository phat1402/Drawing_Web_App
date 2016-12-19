import random
import re

import requests
from django.core.cache import cache
from django.db.models import Count, Max, Avg, F, IntegerField, Sum, Case, When
from django.views import generic
from django.views.generic import FormView
from django.views.generic.base import ContextMixin
from api.models import UserInfor, Photolike, Photo, Followed, Comment
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from forms import DocumentForm
from django.shortcuts import render
from django.http import HttpResponse
import json

def upload_image(request):
    if request.method == 'POST':
        form = DocumentForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            print 'valid form'
            username = request.session['username']
            current_user = UserInfor.objects.get(username=username)
            parts = str(request.FILES['docfile']).split('.')
            if len(parts) != 2:
                data = {'result': 'fail', 'message': 'The image shall not contain many dots'}
            else:
                name = parts[0]
                exts = parts[1]
                if exts.lower() not in ['jpg', 'jpeg', 'png', 'gif']:
                    data = {'result': 'fail', 'message': 'Must select an image file extension'}
                else:
                    current_user.docfile = request.FILES['docfile']
                    current_user.save()
                    request.session['uploaded_photo'] = str(request.FILES['docfile'])
                    data = {'result': 'success', 'message': 'Successfully upload image', 'uploaded_file':str(request.FILES['docfile'])}
            return HttpResponse(json.dumps(data))
    else:
        form = DocumentForm()  # A empty, unbound form
        return render(request, 'mygallery.html', {'form': form})


class HomePage(generic.TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return super(HomePage, self).get(request, *args, **kwargs)


class MyGallery(generic.TemplateView):
    template_name = 'mygallery.html'
    form_class = DocumentForm

    def get(self, request, *args, **kwargs):
        print(request.session.get('username'))
        photos = Photo.objects.filter(username=request.session.get('username'))
        number_of_photos = photos.count()
        kwargs['photos'] = photos
        kwargs['form'] = self.form_class
        kwargs['username'] = request.session.get('username')
        kwargs['numberofphoto'] = number_of_photos
        return super(MyGallery, self).get(request, *args, **kwargs)


class ColoringPage(generic.TemplateView):
    template_name = 'coloringpage.html'

    def get(self, request, *args, **kwargs):
        return super(ColoringPage, self).get(request, *args, **kwargs)


class ImageDetail(generic.TemplateView):
    template_name = 'image_detail.html'

    def get(self, request, *args, **kwargs):
        photo = get_object_or_404(Photo, photo_id=kwargs['photo_id'])
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
        photo = get_object_or_404(Photo, photo_id=kwargs['photo_id'])
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
        photo = get_object_or_404(Photo, photo_id=kwargs['photo_id'])
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
        for user_follow in followeds:
            username_follow = user_follow.followed
            photos = Photo.objects.filter(username=username_follow)
            for photo in photos:
                photo_list.append(photo)

        kwargs['photo_list'] = photo_list
        return super(NewsFeed, self).get(request, *args, **kwargs)


class FriendImageDetail(generic.TemplateView):
    template_name = 'newsfeed_image.html'

    def get(self, request, *args, **kwargs):
        return super(FriendImageDetail, self).get(request, *args, **kwargs)
