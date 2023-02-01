from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import *


class AddProductView(APIView):

    def post(self, request):
        print(request.data)
        product_title = request.data['setProductVariantPrices']
        sku = request.data['product_sku']
        product_description = request.data['product_description']
        product_img = request.data[]
        # save to product
        product = Product.objects.create(title=request.data['product_name'])

        return Response("success")