from django.urls import path, re_path

from product.views import products

from product.views.product import CreateProductView, EditProductView, UpdateProductView
from product.views.variant import VariantView, VariantCreateView, VariantEditView
from .API.apiViews import AddProductView, UpdateProduct

app_name = "product"

urlpatterns = [
    # Variants URLs
    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create', VariantCreateView.as_view(), name='create.variant'),
    path('variant/<int:id>/edit', VariantEditView.as_view(), name='update.variant'),

    # Products URLs
    path('create/', CreateProductView.as_view(), name='create.product'),
    path('product/<int:pk>/edit', EditProductView.as_view(), name='edit.product'),
    path('<int:pk>/update/', UpdateProductView.as_view(), name='update.product'),
    re_path(r'^add/product/$', AddProductView.as_view(), name='add-product'),


    re_path(r'^list/$', products.ProductListView.as_view(), name='product_list'),
    # re_path(r'^list/$', products.product_list, name='product_list'),

    # API urls
    path('<int:pk>/update/product/', UpdateProduct.as_view(), name="getUpateProductApi")
]
