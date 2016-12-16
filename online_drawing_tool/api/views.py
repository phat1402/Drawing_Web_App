from django.views import generic
from braces.views import LoginRequiredMixin, JsonRequestResponseMixin, \
    CsrfExemptMixin, AjaxResponseMixin, JSONResponseMixin
from django.apps import apps
from api.models import UserInfor, Photo, UserGallery, Photolike, Comment
from django.http import HttpResponse
import json
from django.shortcuts import render, render_to_response
from django.template import RequestContext
import random, string
import base64
import os
import time
from os.path import dirname, join, exists
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.template import loader
from django.db.models.query_utils import Q


class ResetPasswordRequestView(generic.View):
    @staticmethod
    def validate_email_address(email):
        '''
        This method here validates the if the input is an email address or not. Its return type is boolean, True if the input is a email address or False if its not.
        '''
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):
        '''
        A normal post request which takes input from field "email_or_username" (in ResetPasswordRequestForm).
        '''
        # form = self.form_class(request.POST)
        email_username = request.POST.get('email_username')
        data = {}
        # if form.is_valid():
        #    data = form.cleaned_data["email_or_username"]
        if self.validate_email_address(email_username) is True:  # uses the method written above
            associated_users = UserInfor.objects.filter(Q(email=email_username) | Q(username=email_username))
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': request.META['HTTP_HOST'],
                        'site_name': "Online Drawing Tool Skyss's",
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'protocol': 'http',
                    }
                    subject_template_name = 'Subject.txt'
                    # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
                    email_template_name = 'passwordresetemail.html'
                    # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
                    subject = loader.render_to_string(subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, 'baileyvstheworld@gmail.com', [user.email], fail_silently=False)
                data = {'result': 'success',
                        'message': 'An email has been sent to ' + email_username + ". Please check its inbox."}
                # messages.success(request, 'An email has been sent to ' + data + ". Please check its inbox to continue reseting password.")
                return HttpResponse(json.dumps(data))
            data = {'result': 'failed',
                    'message': 'No user is associated with this email address'}
            # result = self.form_invalid(form)
            # messages.error(request, 'No user is associated with this email address')
            return HttpResponse(json.dumps(data))
        else:
            associated_users = UserInfor.objects.filter(username=email_username)
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': "Online Drawing Tool Skyss's",  # or your domain
                        'site_name': "Online Drawing Tool Skyss's",
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'protocol': 'http',
                    }
                    subject_template_name = 'registration/password_reset_subject.txt'
                    email_template_name = 'registration/password_reset_email.html'
                    subject = loader.render_to_string(subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, 'baileyvstheworld@gmail.com', [user.email], fail_silently=False)
                data = {'result': 'success',
                        'message': 'An email has been sent to ' + email_username + ". Please check its inbox."}
                # result = self.form_valid(form)
                # messages.success(request, 'Email has been sent to ' + data + "'s email address. Please check its inbox to continue reseting password.")
                return HttpResponse(json.dumps(data))
            # result = self.form_invalid(form)
            # messages.error(request, 'This username does not exist in the system.')
            data = {'result': 'failed',
                    'message': 'No user is associated with this email address'}
            return HttpResponse(json.dumps(data))
            # messages.error(request, 'Invalid Input')
            # return self.form_invalid(form)


class SendLoginAPI(CsrfExemptMixin, JsonRequestResponseMixin, generic.View):
    def post(self, request, *args, **kwargs):

        email = request.POST.get('email')
        password = request.POST.get('pass')

        try:
            userinfo = UserInfor.objects.get(email=request.POST['email'])
        except UserInfor.DoesNotExist:
            userinfo = None

        if userinfo:
            print(userinfo.password)
            if (userinfo.password == request.POST['pass']):
                print("Success")
                request.session['username'] = userinfo.username
                data = {'result': 'sucess', 'username': request.session['username']}
            else:
                print("Failed")
                data = {'result': 'failed', 'messages': 'Sorry! Either your username or password is incorrect'}
        else:
            print("Invalid username")
            data = {'result': 'failed', 'messages': 'Sorry! Either your username or password is incorrect'}

        return HttpResponse(json.dumps(data))


class SendRegisterAPI(CsrfExemptMixin, JsonRequestResponseMixin, generic.View):
    def post(self, request, *args, **kwargs):

        username = request.POST.get('username')
        fullname = request.POST.get('fullname')
        gender = request.POST.get('gender')
        dob = request.POST.get('date_of_birth')
        emailregister = request.POST.get('emailregister')
        passregister = request.POST.get('passregister')
        confirmedpass = request.POST.get('confirmedpass')

        if (gender == 'male'):
            gender_db = 'M'
        elif (gender == 'female'):
            gender_db = 'F'
        else:
            gender_db = 'O'

        try:
            userinfo_username = UserInfor.objects.get(username=request.POST['username'])
        except UserInfor.DoesNotExist:
            userinfo_username = None

        try:
            userinfo_email = UserInfor.objects.get(email=request.POST['emailregister'])
        except UserInfor.DoesNotExist:
            userinfo_email = None
        data = {}
        if (userinfo_username):
            data.update(
                {'result_1': 'ufailed', 'message_1': 'Sorry! This username has already been used. Please try another.'})
        if (userinfo_email):
            data.update(
                {'result_2': 'efailed', 'message_2': 'Sorry! This email has already been used. Please try another.'})
        if (not (userinfo_username) and not (userinfo_email)):
            UserInfor.objects.create(username=username, fullname=fullname, dob=dob, gender=gender_db,
                                     email=emailregister, password=passregister)
            gallery_id = username + '_' + str(int(round(time.time() * 1000)))
            username_obj = UserInfor.objects.get(username=username)
            UserGallery.objects.create(gallery_id=gallery_id, username=username_obj)
            data = {'result': 'success', 'message_3': 'Successfully create new account.'}

        return HttpResponse(json.dumps(data))

    # def autocomplete_search(request):
    #    term = request.GET.get('term') #jquery-ui.autocomplete parameter
    #    photos = Photo.objects.filter(photo_id__istartswith=term) #lookup for a city
    #    res = []
    #    for c in photos:
    #         #make dict with the metadatas that jquery-ui.autocomple needs (the documentation is your friend)
    #         dict = {'photo_id':c.photo_id, 'gallery':c.gallery}
    #         res.append(dict)
    #   return HttpResponse(simplejson.dumps(res))


# def autocompleteModel(request):
#    search_qs = Photo.objects.filter(photo_id__startswith=request.REQUEST['search'])
#    results = []
#    for r in search_qs:
#        results.append(r.name)
#    resp = request.REQUEST['callback'] + '(' + simplejson.dumps(results) + ');'
#    return HttpResponse(resp, content_type='application/json')


def search_titles(request):
    select = 'photo'
    if request.method == 'GET':
        search_text = request.GET.get('search_text')
    else:
        search_text = ''
    if (search_text != ''):
        results_Photo = Photo.objects.filter(photo_name__istartswith=search_text,
                                             username=request.session.get('username'))
    else:
        results_Photo = ''
    return render_to_response('ajax_search.html', {'results': results_Photo, 'select': select})


def log_out(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return render(request, "index.html")


# def like_ajax(request, *args, **kwargs):
#     liked = request.GET.get('liked')
#     post_id = request.GET.get('post_id')
#     num_likes = request.GET.get('num_likes')
#     if strtobool(liked):
#         print('unliked')
#         if int(num_likes) > 0:
#             user_liked = Photolike.objects.get(photo_id=post_id)
#             user_liked.delete()
#             likes = Photolike.objects.filter(photo__photo_id=post_id).count()
#             try:
#                 del request.session[request.session.get('username') + 'has_liked_' + str(post_id)]
#             except KeyError:
#                 print("keyerror")
#             return HttpResponse(likes, liked)
#         else:
#             likes = 0
#             return HttpResponse(likes, liked)
#     else:
#         print("like")
#         liked = True
#         like_id = ''.join(random.choice(string.digits) for i in range(13))
#
#         while(1):
#             if Photolike.objects.filter(like_id=like_id).count()==0:
#                 user_obj = UserInfor.objects.get(username=request.session.get('username'))
#                 Photolike.objects.create(like_id=like_id, photo_id=post_id, username=user_obj)
#                 break
#             else:
#                 like_id = ''.join(random.choice(string.digits) for i in range(13))
#
#         likes = Photolike.objects.filter(photo__photo_id=post_id).count()
#         return HttpResponse(likes, liked)

def like_ajax(request):
    liked = request.GET.get('liked_db')
    post_id = request.GET.get('post_id')
    num_likes = request.GET.get('num_likes')
    # request.session[request.session.get('username') + '_has_liked' + post_id] = False
    print(request.session.get(request.session.get('username') + '_has_liked' + post_id))
    if request.session.get(request.session.get('username') + '_has_liked' + post_id) is None:
        if liked == 'True':
            if int(num_likes) > 0:
                user_liked = Photolike.objects.get(photo_id=post_id)
                user_liked.delete()
                likes = Photolike.objects.filter(photo__photo_id=post_id).count()
                liked = 'False'
                # try:
                #    del request.session[request.session.get('username') + 'has_liked_' + str(post_id)]
                # except KeyError:
                #    print("keyerror")
                data = {'likes': likes, 'liked': liked}
                return HttpResponse(json.dumps(data))
            else:
                liked = 'False'
                likes = 0

                data = {'likes': likes, 'liked': liked}
                return HttpResponse(json.dumps(data))

        else:
            liked = 'True'
            request.session[request.session.get('username') + '_has_liked' + post_id] = True
            like_id = ''.join(random.choice(string.digits) for i in range(13))

            while (1):
                if Photolike.objects.filter(like_id=like_id).count() == 0:
                    user_obj = UserInfor.objects.get(username=request.session.get('username'))
                    Photolike.objects.create(like_id=like_id, photo_id=post_id, username=user_obj)
                    break
                else:
                    like_id = ''.join(random.choice(string.digits) for i in range(13))

            likes = Photolike.objects.filter(photo__photo_id=post_id).count()
            data = {'likes': likes, 'liked': liked}
            return HttpResponse(json.dumps(data))

    if request.session[request.session.get('username') + '_has_liked' + post_id] is True:
        print('unliked')
        likes = Photolike.objects.filter(photo__photo_id=post_id).count()
        if likes > 0:
            liked = 'False'
            user_liked = Photolike.objects.get(photo_id=post_id)
            user_liked.delete()
            likes = Photolike.objects.filter(photo__photo_id=post_id).count()
            try:
                del request.session[request.session.get('username') + '_has_liked' + post_id]
            except KeyError:
                print("keyerror")
            data = {'likes': likes, 'liked': liked}
            return HttpResponse(json.dumps(data))
        else:
            liked = 'False'
            likes = 0
            try:
                del request.session[request.session.get('username') + '_has_liked' + post_id]
            except KeyError:
                print("keyerror")
            data = {'likes': likes, 'liked': liked}
            return HttpResponse(json.dumps(data))


def saveimage(request):
    name = request.POST.get('image_name')
    data_base64 = request.POST.get('data_base64')
    image_name = name + '.png'
    imgData = data_base64.split(',')[1]

    # Generate Path
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # THIS DIRECTORY DEPENDS ON OS
    USERPHOTO_DIRS = join(BASE_DIR, 'static/user_photo/')
    REAL_DIR = USERPHOTO_DIRS + image_name
    message = 'Save Image Successfully'
    with open(REAL_DIR, "wb") as fh:
        fh.write(base64.decodestring(imgData))

    # Get Username infor
    username = request.session['username']

    # Add Infor to database
    photo_id = username + '_' + str(int(round(time.time() * 1000)))
    gallery_id = UserGallery.objects.filter(username=username).values('gallery_id')[0]['gallery_id']
    username_obj = UserInfor.objects.get(username=username)
    photo_link = '/static/user_photo/' + image_name
    Photo.objects.create(photo_id=photo_id, gallery_id=gallery_id, photo_link=photo_link, photo_name=name,
                         username=username_obj)

    return HttpResponse(message)


def comment(request):
    comment_db = request.GET.get('comment_text')
    photo_id_text = request.GET.get('photo_id')
    username_to_input_comment_db = UserInfor.objects.get(username=request.session.get('username'))
    # photo_id_to_input_comment_db = Photo.objects.get(photo_id=photo_id_text)
    comment_id_text = ''.join(random.choice(string.digits) for i in range(13))
    while (1):
        if Comment.objects.filter(comment_id=comment_id_text).count() == 0:
            Comment.objects.create(comment_id=comment_id_text, content=comment_db,
                                   username=username_to_input_comment_db, photo_id=photo_id_text)
            break
        else:
            comment_id_text = ''.join(random.choice(string.digits) for i in range(13))
            # comment_input_db = request.session.get('username') + '-' + comment_id_text
    data = {'user_has_commented': request.session.get('username'), 'comment_input': comment_db}
    return HttpResponse(json.dumps(data))
