from django.shortcuts import render, redirect

def product_list(request):

    return render(request, 'products/list.html')
