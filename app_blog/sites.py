# -*- coding: utf-8 -*-

from django.contrib.admin.sites import AdminSite as _AdminSite

from app_blog.forms.auth import AuthForm


class AdminSite(_AdminSite):
    """
    overwrite the default AdminSite from django
    to modify the login form with adding new recaptcha field.
    """
    login_template = 'app_blog/admin/login.html'
    login_form = AuthForm
