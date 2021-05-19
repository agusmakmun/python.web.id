# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import (get_object_or_404, redirect)
from django.views.generic import (TemplateView, ListView, DetailView,
                                  FormView, UpdateView)
from django.db.models import Q

from apps.product.models.product import Product
from apps.product.forms.product import ProductForm
from apps.blog.utils.json import JSONResponseMixin
from apps.blog.utils.visitor import visitor_counter
from apps.accounts.utils.mixins import StaffLoginRequiredMixin
from apps.blog.models.addons import Visitor


class ProductListView(ListView):
    template_name = 'apps/product/list.html'
    queryset = Product.objects.published()
    context_object_name = 'products'
    paginate_by = 9

    def get_default_queryset(self):
        """ need this to implement overwrite the default queryset """
        return self.queryset

    def get_queryset(self):
        queryset = self.get_default_queryset()
        self.query = self.request.GET.get('q')

        if self.query:
            queryset = queryset.filter(Q(title__icontains=self.query))

        return queryset

    @property
    def extra_context(self):
        """ additional `context_data` for `get_context_data` """
        return None

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['query'] = self.query
        if self.extra_context:
            context_data.update(**self.extra_context)
        return context_data


class ProductListAuthorPrivateView(StaffLoginRequiredMixin, ProductListView):
    template_name = 'apps/product/list_private.html'

    def get_default_queryset(self):
        queryset = self.queryset.filter(author=self.request.user)
        self.publish = self.request.GET.get('publish')

        if self.publish == 'yes':
            queryset = queryset.filter(publish=True)
        elif self.publish == 'no':
            queryset = queryset.filter(publish=False)

        return queryset

    @property
    def extra_context(self):
        return dict(publish=self.publish)


class ProductDetailView(DetailView):
    template_name = 'apps/product/detail.html'
    context_object_name = 'product'
    model = Product

    def get_object(self):
        queries = {'id': self.kwargs['id'], 'deleted_at__isnull': True}
        return get_object_or_404(self.model, **queries)

    def get_visitors(self):
        """
        function to get/create the visitor,
        :return dict of {'client_ip': <str>, 'total_visitors': <int>}
        """
        queries = {'request': self.request,
                   'content_type': self.object.get_content_type(),
                   'object_id': self.object.id}
        return visitor_counter(**queries)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['visitor_counter'] = self.get_visitors()
        return context_data


class ProductCreateView(StaffLoginRequiredMixin, FormView):
    template_name = 'apps/product/create.html'
    form_class = ProductForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()
        form.save()
        messages.success(self.request, _('Product successfully created!'))
        return redirect(reverse('apps.product:product_detail', kwargs={'id': instance.id}))


class ProductUpdateView(StaffLoginRequiredMixin, UpdateView):
    template_name = 'apps/product/update.html'
    context_object_name = 'product'
    form_class = ProductForm
    model = Product

    def get_object(self):
        """ handle the object for specific permission """
        if self.request.user.is_superuser:
            return get_object_or_404(self.model, id=self.kwargs['id'])
        return get_object_or_404(self.model, id=self.kwargs['id'], author=self.request.user)

    def form_valid(self, form):
        product = self.get_object()
        instance = form.save(commit=False)
        instance.author = product.author
        instance.save()
        form.save()
        message = _('"%(product)s" successfully updated!') % {'product': instance}
        messages.success(self.request, message)
        return redirect(reverse('apps.product:product_detail', kwargs={'id': instance.id}))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['product'] = self.get_object()
        return context


class ProductDeleteJSONView(JSONResponseMixin, TemplateView):
    model = Product

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object = None

    def get_object(self, id):
        if not self.object:
            self.object = get_object_or_404(self.model, id=id)
        return self.object

    def soft_delete_product(self, id):
        """
        function to delete the product object with soft delete method
        :param `id` is integer id of `Product`.
        """
        # soft delete the related objects
        queries = {'content_type__model': 'product', 'object_id': id}
        Visitor.objects.filter(**queries).update(deleted_at=timezone.now())

        # soft delete the object
        product = self.get_object(id)
        product.deleted_at = timezone.now()
        product.save()

        return True

    def get(self, request, *args, **kwargs):
        context_data = {'success': False, 'message': None}
        id = request.GET.get('id')

        if str(id).isdigit():
            if not request.user.is_authenticated:
                context_data['message'] = _('You must login to delete this product!')
            elif request.user.is_superuser:
                self.soft_delete_product(id)
                context_data['success'] = True
                context_data['message'] = _('The product successfully deleted!')
            elif request.user != self.get_object(id).author:
                context_data['message'] = _('You are not allowed to access this feature!')
            else:
                self.soft_delete_product(id)
                context_data['success'] = True
                context_data['message'] = _('The product successfully deleted!')
        else:
            context_data['message'] = _('Param `id` should be integer!')

        return self.render_to_json_response(context_data)
