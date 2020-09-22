# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.db.models import (Q, F, Count)
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import (get_object_or_404, redirect)
from django.views.generic import (ListView, DetailView,
                                  FormView, UpdateView)

from apps.product.models.product import Product
from apps.product.forms.product import ProductForm
from apps.accounts.utils.mixins import StaffLoginRequiredMixin


class ProductListView(ListView):
    template_name = 'apps/product/list.html'
    queryset = Product.objects.published()
    context_object_name = 'products'
    paginate_by = 9


class ProductDetailView(DetailView):
    template_name = 'apps/product/detail.html'
    context_object_name = 'product'
    model = Product

    def get_object(self):
        queries = {'id': self.kwargs['id'], 'deleted_at__isnull': True}
        return get_object_or_404(self.model, **queries)


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
