from ..models import Product, ProductImage, ProductVariant, ProductVariantPrice, Variant
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views import View
from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Q
from datetime import datetime
from django.utils import timezone


# Q(loc__icontains=value) | Q(loc_mansioned__icontains=value) | Q(loc_country__icontains=value) | Q(loc_modern__icontains=value)



class ProductListView(ListView):
    model = ProductVariantPrice
    template_name = 'products/list.html'
    context_object_name = 'products'
    queryset = ProductVariantPrice.objects.all()
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        print(self.kwargs)
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['varients'] = Variant.objects.all()
        return context

    def get_queryset(self):
        print(self.request)
        title = self.request.GET.get('title', '')
        varient = self.request.GET.get('variant')
        print(varient)
        price_range_1 = self.request.GET.get('price_from')
        price_range_2 = self.request.GET.get('price_to')
        date = self.request.GET.get('date', '')
        if title or varient or price_range_1 or price_range_2 or date:
            price_range_1_to_float = 0
            price_range_2_to_float = 0
            varient_pk = None
            filter_by_date = datetime.now()
            if date:
                filter_by_date = timezone.datetime.strptime(date, '%Y-%m-%d')


            if varient:
                varient_pk = int(varient)

            if price_range_1:
                price_range_1_to_float = float(price_range_1)
            if price_range_2:
                price_range_2_to_float = float(price_range_2)

            products = ProductVariant.objects.filter(Q(product__title__iexact=title) | (Q(product__created_at__year=filter_by_date.year) & Q(product__created_at__month=filter_by_date.month) & Q(product__created_at__day=filter_by_date.day)) | Q(variant__pk__exact=varient_pk) | Q(price__range=(price_range_1_to_float, price_range_2_to_float))).order_by('pk')
            print(products)
            print(ProductVariant.objects.filter())
            return ProductVariantPrice.objects.filter(Q(product_varients__in=products)).order_by('pk').distinct()
        else:
            return ProductVariantPrice.objects.all().order_by('pk')

def product_list(request):

    return render(request, 'products/list.html')
