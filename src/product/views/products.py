from ..models import Product, ProductImage, ProductVariant, ProductVariantPrice, Variant
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views import View
from django.db.models import Q
from datetime import datetime
from django.utils import timezone


class ProductListView(ListView):
    model = ProductVariantPrice
    template_name = 'products/list.html'
    context_object_name = 'products'
    queryset = ProductVariantPrice.objects.all()
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        title = self.request.GET.get('title', '')
        varient = self.request.GET.get('variant', '')
        price_range_1 = self.request.GET.get('price_from')
        price_range_2 = self.request.GET.get('price_to')
        date = self.request.GET.get('date', '')

        print(title)
        print(varient)
        print(price_range_1)
        print(price_range_2)
        print(date)
        if title or varient or price_range_1 or price_range_2 or date:
            price_range_1_to_float = 0
            price_range_2_to_float = 0

            product_by_title = []
            product_by_date_rage = []
            product_by_price_range = []
            product_by_variant = []

            if title:
                product_by_title = ProductVariant.objects.filter(Q(product__title__contains=title))

            filter_by_date = datetime.now()
            if date:
                filter_by_date = timezone.datetime.strptime(date, '%Y-%m-%d')
                product_by_date_rage = ProductVariant.objects.filter(
                    Q(product__created_at__year=filter_by_date.year) & Q(
                        product__created_at__month=filter_by_date.month) & Q(
                        product__created_at__day=filter_by_date.day))

            if price_range_1:
                price_range_1_to_float = float(price_range_1)
            if price_range_2:
                price_range_2_to_float = float(price_range_2)

            if price_range_1_to_float and price_range_2_to_float:
                product_by_price_range = ProductVariant.objects.filter(
                    Q(price__range=(price_range_1_to_float, price_range_2_to_float)))


            if varient:
                product_by_variant = ProductVariant.objects.filter(Q(variant_title__icontains=varient))
                print(product_by_variant)

            filtered_products = [*product_by_title, *product_by_price_range, *product_by_variant, *product_by_date_rage]
            return ProductVariantPrice.objects.filter(Q(product_varients__in=filtered_products)).order_by('pk').distinct()
        else:
            return ProductVariantPrice.objects.all().order_by('pk')

