# -*- coding: utf-8 -*-

from django.contrib.admin.sites import AdminSite as _AdminSite

from apps.blog.forms.auth import AuthAdminForm


class AdminSite(_AdminSite):
    """
    overwrite the default AdminSite from django
    to modify the login form with adding new recaptcha field.
    """
    login_template = 'apps/blog/admin/login.html'
    login_form = AuthAdminForm
