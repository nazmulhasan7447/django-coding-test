from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from .serializer import *


class AddProductView(APIView):

    def post(self, request):
        try:
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
                    variant_title=variant['title'],
                    product=product,
                    price=variant['price'],
                    stock=variant['stock']
                )
                product_variant_price_model.product_varients.add(product_variant)
                product_variant_price_model.save()

            return Response("success")
        except:
            return Response("Something went wrong")


class UpdateProduct(APIView):

    def get(self, request, *args, **kwargs):
        current_product = get_object_or_404(ProductVariantPrice, pk=kwargs.get('pk'))
        serializers = ProductVarientPriceSerializer(current_product, many=False)

        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            current_product = get_object_or_404(ProductVariantPrice, pk=kwargs.get('pk'))

            product_title = request.data['title']
            sku = request.data['sku']
            product_description = request.data['description']
            variants = request.data['variants']

            current_product.product.title = product_title
            current_product.product.sku = sku
            current_product.product.description = product_description
            current_product.product.save()

            for variant in variants:
                product_variant = current_product.product_varients.get(pk=variant['id'])
                product_variant.price= variant['price']
                product_variant.stock= variant['stock']
                product_variant.save()


            return Response("success")
        except:
            return Response("Something went wrong")



