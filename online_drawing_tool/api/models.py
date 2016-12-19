# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Coloringbook(models.Model):
    uploadedphoto = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'coloringbook'


class Comment(models.Model):
    comment_id = models.CharField(primary_key=True, max_length=40)
    content = models.TextField(blank=True, null=True)
    username = models.ForeignKey('UserInfor', models.DO_NOTHING, db_column='username', blank=True, null=True)
    photo = models.ForeignKey('Photo', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Followed(models.Model):
    fed_id = models.IntegerField(primary_key=True)
    username = models.ForeignKey('UserInfor', models.DO_NOTHING, db_column='username', blank=True, null=True)
    followed = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'followed'


class Following(models.Model):
    fing_id = models.IntegerField(primary_key=True)
    username = models.ForeignKey('UserInfor', models.DO_NOTHING, db_column='username', blank=True, null=True)
    follower = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'following'


class Photo(models.Model):
    photo_id = models.CharField(primary_key=True, max_length=100)
    gallery = models.ForeignKey('UserGallery', models.DO_NOTHING, blank=True, null=True)
    photo_link = models.CharField(max_length=1000, blank=True, null=True)
    username = models.ForeignKey('UserInfor', models.DO_NOTHING, db_column='username', blank=True, null=True)
    photo_name = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'photo'


class Photolike(models.Model):
    like_id = models.CharField(primary_key=True, max_length=30)
    photo = models.ForeignKey(Photo, models.DO_NOTHING, blank=True, null=True)
    username = models.ForeignKey('UserInfor', models.DO_NOTHING, db_column='username', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'photolike'

class Report(models.Model):
    report_id = models.CharField(primary_key=True, max_length=30)
    username = models.ForeignKey('UserInfor', models.DO_NOTHING, related_name='userinfo', db_column='username',
                                     blank=True, null=True)
    reported_username = models.ForeignKey('UserInfor', models.DO_NOTHING, related_name='reported_username',
                                              db_column='reported_username', blank=True, null=True)
    reported_photoid = models.ForeignKey(Photo, models.DO_NOTHING, db_column='reported_photoid', blank=True,
                                             null=True)

    class Meta:
        managed = False
        db_table = 'report'


class UserGallery(models.Model):
    gallery_id = models.CharField(primary_key=True, max_length=100)
    username = models.ForeignKey('UserInfor', models.DO_NOTHING, db_column='username', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_gallery'


class UserInfor(models.Model):
    username = models.CharField(primary_key=True, max_length=40)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    dob = models.CharField(db_column='DOB', max_length=10, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(max_length=1, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    avatar_link = models.CharField(max_length=255, blank=True, null=True)
    report_num = models.IntegerField(blank=True, null=True)
    isadmin = models.IntegerField(blank=True, null=True)
    docfile = models.FileField(upload_to='documents', null=True)
    class Meta:
        managed = True
        db_table = 'user_infor'
