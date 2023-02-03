from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import *


class AddProductView(APIView):
    # {
    #     'product_name': 'Product name',
    #     'product_sku': 'product sku',
    #     'product_description': 'description',
    #     'productVariantPrices': [{'index': 0, 'title': 'red/sm/', 'price': '10', 'stock': '10'
    #                            }, {'index': 1, 'title': 'red/xs/', 'price': '20', 'stock': '20'}]}

    def post(self, request):
        # productImg = ProductImage.objects.create(img=request.data['product_img']["path"])
        product_title = request.data['product_name']
        sku = request.data['product_sku']
        product_description = request.data['product_description']
        product_variants = request.data['productVariantPrices']
        # save to product
        product = Product.objects.create(title=product_title, sku=sku, description=product_description)
        product_variant_price_model = ProductVariantPrice.objects.create(
            product=product
        )
        # product_variant = ProductVariant.objects.create()
        print(product_variants)
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