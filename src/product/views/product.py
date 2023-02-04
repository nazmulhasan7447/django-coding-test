from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from ..models import *
from django.views.generic.edit import UpdateView
import json
from ..API.serializer import *
from rest_framework.response import Response


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


class UpdateProductView(generic.TemplateView):
    template_name = 'products/update.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['variants'] = list(variants.all())
        return context