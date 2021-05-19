"""
Dashboard Index Views
to show all statistics.
"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
from django.views.generic import TemplateView

from core.utils.mixins import SuperUserLoginRequiredMixin

from apps.accounts.models.user import User
from apps.blog.models.addons import Visitor
from apps.blog.models.post import Post
from apps.blog.models.tag import Tag


class DashboardIndexView(SuperUserLoginRequiredMixin, TemplateView):
    template_name = 'apps/dashboard/index.html'
    now = timezone.now()

    def get_total_tags(self, period: str, month: int = None) -> int:
        """
        function to get the total tags per-month / year.
        :param `period` is string period (choices: "year", "month")
        :param `month` is optional integer month if it period as "month".
        :return int total of tags.
        """
        if period == 'year':
            return Tag.objects.filter(
                created_at__year=self.now.year
            ).count()
        elif period == 'month':
            return Tag.objects.filter(
                created_at__year=self.now.year,
                created_at__month=month
            ).count()
        return 0

    def get_total_users(self, period: str, month: int = None) -> int:
        """
        function to get the total users per-month / year.
        :param `period` is string period (choices: "year", "month")
        :param `month` is optional integer month if it period as "month".
        :return int total of users
        """
        if period == 'year':
            return User.objects.filter(
                date_joined__year=self.now.year
            ).count()
        elif period == 'month':
            return User.objects.filter(
                date_joined__year=self.now.year,
                date_joined__month=month
            ).count()
        return 0

    def get_total_posts(self, period: str, month: int = None) -> int:
        """
        function to get the total posts per-month / year.
        :param `period` is string period (choices: "year", "month")
        :param `month` is optional integer month if it period as "month".
        :return int total of posts.
        """
        if period == 'year':
            return Post.objects.filter(
                created_at__year=self.now.year
            ).count()
        elif period == 'month':
            return Post.objects.filter(
                created_at__year=self.now.year,
                created_at__month=month
            ).count()
        return 0

    def get_total_visitors(self, period: str, month: int = None) -> int:
        """
        function to get the total visitors per-month / year.
        :param `period` is string period (choices: "year", "month")
        :param `month` is optional integer month if it period as "month".
        :return int total of visitors.
        """
        if period == 'year':
            return Visitor.objects.filter(
                created_at__year=self.now.year
            ).count()
        elif period == 'month':
            return Visitor.objects.filter(
                created_at__year=self.now.year,
                created_at__month=month
            ).count()
        return 0

    def get_data_visitors_per_months(self) -> list:
        """
        function to get the calculate the total data
        of visitors for each month.
        :return list dict of data per month.
        """
        data_per_months = []
        for month in range(1, 12):
            total = self.get_total_visitors(period='month', month=month)
            data_per_months.append(total)
        return data_per_months

    def get_data_per_months(self) -> list:
        """
        function to get the calculate the total data
        includes (user, product) for each month.
        :return list dict of data per month.
        """
        data_per_months = []
        for month in range(1, 12):
            data_per_months.append({
                'tag': self.get_total_tags(period='month', month=month),
                'post': self.get_total_posts(period='month', month=month),
                'user': self.get_total_users(period='month', month=month)
            })
        return data_per_months

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['total_tags'] = Tag.objects.all().count()
        context_data['total_tags_this_year'] = self.get_total_tags(period='year')
        context_data['total_users'] = User.objects.all().count()
        context_data['total_users_this_year'] = self.get_total_users(period='year')
        context_data['total_posts'] = Post.objects.all().count()
        context_data['total_posts_this_year'] = self.get_total_posts(period='year')
        context_data['total_visitors'] = Visitor.objects.all().count()
        context_data['total_visitors_this_year'] = self.get_total_visitors(period='year')
        context_data['data_visitors_per_months'] = self.get_data_visitors_per_months()
        context_data['data_per_months'] = self.get_data_per_months()
        return context_data
