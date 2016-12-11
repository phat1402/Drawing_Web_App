from django.views import generic
from braces.views import LoginRequiredMixin, JsonRequestResponseMixin, \
    CsrfExemptMixin, AjaxResponseMixin, JSONResponseMixin
from django.apps import apps
from api.models import UserInfor,Photo,UserGallery,Photolike
from django.http import HttpResponse
import json as simplejson
from django.shortcuts import render_to_response
from models import UserInfor
from django.http import HttpResponse
import json
from django.shortcuts import render, render_to_response
from django.template import RequestContext
import random, string
from distutils.util import strtobool
import base64
import os
import time
from os.path import dirname, join, exists

class SendLoginAPI(CsrfExemptMixin,JsonRequestResponseMixin, generic.View):

    def post(self, request, *args, **kwargs):

        email = request.POST.get('email')
        password = request.POST.get('pass')

        print request.is_ajax()
        print(email)
        print(password)
        try:
            userinfo = UserInfor.objects.get(email=request.POST['email'])
        except UserInfor.DoesNotExist:
            userinfo = None

        if userinfo:
            print (userinfo.password)
            if (userinfo.password == request.POST['pass']):
                print("Success")
                request.session['username'] = userinfo.username
                data = {'result':'sucess','username': request.session['username']}
            else:
                print("Failed")
                data = {'result': 'failed', 'messages' : 'Sorry! Either your username or password is incorrect'}
        else:
            print("Invalid username")
            data = {'result': 'failed', 'messages': 'Sorry! Either your username or password is incorrect'}
        print data['result']

        return HttpResponse(json.dumps(data))

class SendRegisterAPI(CsrfExemptMixin,JsonRequestResponseMixin, generic.View):

    def post(self, request, *args, **kwargs):

        username = request.POST.get('username')
        fullname = request.POST.get('fullname')
        emailregister = request.POST.get('emailregister')
        passregister = request.POST.get('passregister')
        confirmedpass = request.POST.get('confirmedpass')
        address = request.POST.get('address')


        print(username)
        print(fullname)
        print(emailregister)
        print(passregister)
        print(confirmedpass)
        print(address)

        try:
            userinfo_username = UserInfor.objects.get(username=request.POST['username'])
        except UserInfor.DoesNotExist:
            userinfo_username = None

        try:
            userinfo_email = UserInfor.objects.get(username=request.POST['emailregister'])
        except UserInfor.DoesNotExist:
            userinfo_email = None

        if (not(userinfo_username) and not(userinfo_email)):
            UserInfor.objects.create(username=username, fullname=fullname, email=emailregister,password=passregister)
        else:
            print("The username or email is already existent")
        return self.render_json_response({
            'success': True})


#def autocomplete_search(request):
#    term = request.GET.get('term') #jquery-ui.autocomplete parameter
#    photos = Photo.objects.filter(photo_id__istartswith=term) #lookup for a city
#    res = []
#    for c in photos:
#         #make dict with the metadatas that jquery-ui.autocomple needs (the documentation is your friend)
#         dict = {'photo_id':c.photo_id, 'gallery':c.gallery}
#         res.append(dict)
 #   return HttpResponse(simplejson.dumps(res))


#def autocompleteModel(request):
#    search_qs = Photo.objects.filter(photo_id__startswith=request.REQUEST['search'])
#    results = []
#    for r in search_qs:
#        results.append(r.name)
#    resp = request.REQUEST['callback'] + '(' + simplejson.dumps(results) + ');'
#    return HttpResponse(resp, content_type='application/json')


def search_titles(request):
    if request.method == 'GET':
        search_text = request.GET['search_text']
    else:
        search_text = ''
    if (search_text != ''):
        results_Photo = Photo.objects.filter(photo_id__istartswith = search_text)
    else:
        results_Photo =''
    return render_to_response('ajax_search.html', {'results':results_Photo})

def log_out(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return render(request,"index.html")

def like_ajax(request, *args, **kwargs):
    liked = request.GET.get('liked')
    post_id = request.GET.get('post_id')
    num_likes = request.GET.get('num_likes')
    if strtobool(liked):
        print('unliked')
        if int(num_likes) > 0:
            user_liked = Photolike.objects.get(photo_id=post_id)
            user_liked.delete()
            likes = Photolike.objects.filter(photo__photo_id=post_id).count()
            try:
                del request.session[request.session.get('username') + 'has_liked_' + str(post_id)]
            except KeyError:
                print("keyerror")
            return HttpResponse(likes, liked)
        else:
            likes = 0
            return HttpResponse(likes, liked)
    else:
        print("like")
        liked = True
        like_id = ''.join(random.choice(string.digits) for i in range(13))

        while(1):
            if Photolike.objects.filter(like_id=like_id).count()==0:
                user_obj = UserInfor.objects.get(username=request.session.get('username'))
                Photolike.objects.create(like_id=like_id, photo_id=post_id, username=user_obj)
                break
            else:
                like_id = ''.join(random.choice(string.digits) for i in range(13))

        likes = Photolike.objects.filter(photo__photo_id=post_id).count()
        return HttpResponse(likes, liked)

def saveimage(request):
    name = request.POST.get('image_name')
    data_base64 = request.POST.get('data_base64')
    image_name = name + '.png'
    imgData = data_base64.split(',')[1]

    #Generate Path
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # THIS DIRECTORY DEPENDS ON OS
    USERPHOTO_DIRS = join(BASE_DIR, 'static/user_photo/')
    REAL_DIR = USERPHOTO_DIRS + image_name
    message = 'Save Image Successfully'
    with open(REAL_DIR, "wb") as fh:
        fh.write(base64.decodestring(imgData))

    #Get Username infor
    username = request.session['username']

    #Add Infor to database
    photo_id = username+ '_' + str(int(round(time.time() * 1000)))
    gallery_id = UserGallery.objects.filter(username=username).values('gallery_id')[0]['gallery_id']
    username_obj = UserInfor.objects.get( username = username)
    print gallery_id
    Photo.objects.create(photo_id = photo_id, gallery_id=gallery_id, photo_link=image_name, username=username_obj)
    print 'Generate Database'

    return HttpResponse(message)


