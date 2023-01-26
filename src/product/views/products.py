from ..models import Product, ProductImage, ProductVariant, ProductVariantPrice
from django.shortcuts import render, redirect
from django.views.generic.list import ListView


class ProductListView(ListView):
    model = ProductVariantPrice
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 3

    # def get_queryset(self):
    #
    #     return Product.objects.all()

def product_list(request):

    return render(request, 'products/list.html')
