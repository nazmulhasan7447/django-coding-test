from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import *


class AddProductView(APIView):

    def post(self, request):
        product_title = request.data['product_name']
        sku = request.data['product_sku']
        product_description = request.data['product_description']
        product_variants = request.data['productVariantPrices']
        # save to product
        product = Product.objects.create(title=product_title, sku=sku, description=product_description)
        product_variant_price_model = ProductVariantPrice.objects.create(
            product=product
        )
        for variant in product_variants:
            product_variant = ProductVariant.objects.create(
                variant_title= variant['title'],
                product= product,
                price=variant['price'],
                stock=variant['stock']
            )
            product_variant_price_model.product_varients.add(product_variant)
            product_variant_price_model.save()



        return Response("success")