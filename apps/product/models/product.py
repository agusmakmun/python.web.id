# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from apps.blog.models.base import (TimeStampedModel, DefaultManager,
                                   ContentTypeModel)
from apps.accounts.models.user import User


class ProductManager(DefaultManager):

    def published(self):
        """ update publish manager for post """
        queryset = super().published()
        return queryset.filter(publish=True)


class Product(TimeStampedModel, ContentTypeModel):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=200)

    class CategoryOptions(models.TextChoices):
        plugin = 'plugin', _('Plugin')
        website = 'website', _('Website')
        ebook = 'ebook', _('E-Book')

    category = models.CharField(_('Category'), max_length=20,
                                choices=CategoryOptions.choices,
                                default=CategoryOptions.plugin)

    class TypeOptions(models.TextChoices):
        premium = 'premium', _('Premium')
        free = 'free', _('Free')

    type = models.CharField(_('Type'), max_length=20,
                            choices=TypeOptions.choices,
                            default=TypeOptions.premium)

    price = models.PositiveIntegerField(_('Price'), default=0,
                                        help_text=_('Currently price, e.g: 75000'))
    price_discount = models.PositiveIntegerField(_('Price Discount'), null=True, blank=True,
                                                 help_text=_('Fixed price after discount'))

    class CurrencyOptions(models.TextChoices):
        usd = 'usd', _('USD $')
        idr = 'idr', _('IDR Rp')
        sgd = 'sgd', _('SGD S$')
        gbp = 'gbp', _('GBP £')
        eur = 'eur', _('EUR €')

    currency_code = models.CharField(_('Currency Code'), max_length=5,
                                     choices=CurrencyOptions.choices,
                                     default=CurrencyOptions.usd,
                                     help_text=_('Price currency code'))

    buy_url = models.URLField(_('Buy URL'), null=True, blank=True,
                              help_text=_('e.g: https://www.paypal.com/paypalme/summonagus'))
    image_urls = models.TextField(_("Image URL's"), blank=True,
                                  help_text=_('Please use list string format, '
                                              'e.g: ["https://google.com/image.png"]'))
    demo_url = models.URLField(_('Demo URL'), null=True, blank=True)
    download_url = models.URLField(_('Download URL'), null=True, blank=True)
    publish = models.BooleanField(_('Publish'), default=True)
    sort_description = models.TextField(_('Sort Description'))
    long_description = models.TextField(_('Long Description'), blank=True)
    terms_of_service = models.TextField(_('Terms of Service'), blank=True)

    objects = ProductManager()

    def __str__(self):
        return self.title

    @property
    def currency_code_label(self):
        """ function to get the currency code icon, e.g: $, Rp, £ """
        code = getattr(self.CurrencyOptions, self.currency_code)
        print('code', code)
        if code and hasattr(code, 'label'):
            if code.label:
                return code.label.split(' ')[-1]
        return

    @property
    def list_image_urls(self):
        try:
            return eval(self.image_urls)
        except Exception:
            pass
        return []

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ('-created_at',)
