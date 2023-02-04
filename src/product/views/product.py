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
        print(kwargs)
        print(self.kwargs)
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


class UpdateProductView(generic.TemplateView):
    template_name = 'products/update.html'

    def get_context_data(self, **kwargs):
        print(kwargs)
        print(self.kwargs)
        context = super(UpdateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['variants'] = list(variants.all())
        return context


class EditProductView(generic.TemplateView):
    template_name = 'products/edit.html'
    model = ProductVariantPrice

    def get_context_data(self, **kwargs):
        print(kwargs)
        print(self.kwargs)
        context = super(EditProductView, self).get_context_data(**kwargs)
        context['current_product'] = get_object_or_404(ProductVariantPrice, pk=kwargs.get('pk'))
        print(context)

    #     variants = ProductVariantPrice.objects.all()
    #     context['product'] = True
    #     context['variants'] = list(variants.all())
        return context

    def post(self, request, *args, **kwargs):
        print(self.request.POST.get('price'))
        print(args)
        print(kwargs)
        context = self.get_context_data(**kwargs)
        # Your code here

        # bar = self.request.POST.get('foo', None)
        # if bar:
        #     self.template_name = 'path-to-new-template.html'
        # previous_foo = context['foo']
        context['new_variable'] = 'new_variable' + ' updated'

        return redirect('product:product_list')
