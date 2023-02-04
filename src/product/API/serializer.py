from rest_framework import serializers
from ..models import *
from rest_framework import status


class ProductVariantSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariant
        exclude = ('variant',)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['title', 'sku', 'description']

class ProductVarientPriceSerializer(serializers.ModelSerializer):
    product_varients = ProductVariantSerializer(many=True)

    class Meta:
        model = ProductVariantPrice
        fields = ['product', 'product_varients']

    def to_representation(self, instance):
        self.fields['product'] = ProductSerializer(read_only=True)
        return super(ProductVarientPriceSerializer, self).to_representation(instance)
