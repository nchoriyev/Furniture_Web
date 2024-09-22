from itertools import product

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
import requests
from django.contrib import messages
from django.conf import settings


class IndexView(View):
    def get(self, request):
        access_token = request.COOKIES.get('access_token')

        if not access_token:
            return HttpResponseRedirect('auth/login')

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.get('http://127.0.0.3:8003/identify/token/verify', headers=headers)

        if response.status_code == 200:
            username = request.user.username  # Get the logged-in user's username
            return render(request, 'index.html', {'username': username})
        elif response.status_code == 401:
            response = HttpResponseRedirect('/login/')
            response.delete_cookie('access_token')
            return response
        else:
            return HttpResponse("Noma'lum xato yuz berdi", status=500)


class ShopView(View):
    def get(self, request):
        access_token = request.COOKIES.get('access_token')

        if not access_token:
            return HttpResponseRedirect('/auth/login/')

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.get('http://127.0.0.3:8003/identify/token/verify', headers=headers)

        if response.status_code == 200:
            return render(request, 'shop.html')
        else:
            response = HttpResponseRedirect('/auth/login/')
            response.delete_cookie('access_token')
            return response

    def shop_view(request):
        api_url = f"http://127.0.0.3:8003/products/"
        headers = {
            'Authorization': f"Bearer {request.COOKIES.get('access_token')}"
        }

        response = requests.get(api_url, headers=headers)
        products = response.json() if response.status_code == 200 else []

        return render(request, 'shop.html', {'products': products})

    def post(self, request):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return HttpResponseRedirect('/auth/login/')

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        admin_check_response = requests.get('http://127.0.0.3:8003/identify/token/verify', headers=headers)
        if admin_check_response.status_code == 200:
            product_data = {
                'name': request.POST.get('name'),
                'description': request.POST.get('description'),
                'price1': request.POST.get('price1'),
                'price2': request.POST.get('price2'),
                'material': request.POST.get('material'),
                'count': request.POST.get('count'),
                'slug': request.POST.get('slug')
            }

            create_response = requests.post('http://127.0.0.3:8003/products/create', headers=headers, json=product_data)

            if create_response.status_code == 201:
                messages.success(request, "Product created successfully!")
            else:
                messages.error(request, "Failed to create product.")

            return HttpResponseRedirect('/shop/')
        else:
            return HttpResponse("You are not authorized to create a product.", status=403)

    def put(self, request, product_id):
        # Product update (PUT or PATCH)
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return HttpResponseRedirect('/auth/login/')

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        # Admin check for updating
        admin_check_response = requests.get('http://127.0.0.3:8003/identify/token/verify', headers=headers)
        if admin_check_response.status_code == 200:
            # Get data from request body
            product_data = {
                'name': request.POST.get('name'),
                'description': request.POST.get('description'),
                'price1': request.POST.get('price1'),
                'price2': request.POST.get('price2'),
                'material': request.POST.get('material'),
                'country_id': request.POST.get('country_id'),
                'count': request.POST.get('count')
            }

            update_response = requests.put(f'http://127.0.0.3:8003/products/{product_id}/', headers=headers,
                                           json=product_data)

            if update_response.status_code == 200:
                messages.success(request, "Product updated successfully!")
            else:
                messages.error(request, "Failed to update product.")

            return HttpResponseRedirect('/shop/')
        else:
            return HttpResponse("You are not authorized to update this product.", status=403)

    def delete(self, request, product_id):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return HttpResponseRedirect('/auth/login/')

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        # Admin check for deleting
        admin_check_response = requests.get('http://127.0.0.3:8003/identify/token/verify', headers=headers)
        if admin_check_response.status_code == 200:
            delete_response = requests.delete(f'http://127.0.0.3:8003/products/{product_id}/', headers=headers)

            if delete_response.status_code == 204:
                messages.success(request, "Product deleted successfully!")
            else:
                messages.error(request, "Failed to delete product.")

            return HttpResponseRedirect('/shop/')
        else:
            return HttpResponse("You are not authorized to delete this product.", status=403)


class ProductCreateView(View):
    def get(self, request):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return HttpResponseRedirect('/auth/login/')

        return render(request, 'create_product.html')

    def post(self, request):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return HttpResponseRedirect('/auth/login/')

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        # Check if the logged-in user is an admin
        admin_check_response = requests.get('http://127.0.0.3:8003/identify/token/verify', headers=headers)
        if admin_check_response.status_code == 200:
            # Admin can create a product
            product_data = {
                'name': request.POST.get('name'),
                'description': request.POST.get('description'),
                'image': request.POST.get('image'),
                'price1': request.POST.get('price1'),
                'price2': request.POST.get('price2'),
                'material': request.POST.get('material'),
                'country_id': request.POST.get('country_id'),
                'count': request.POST.get('count')
            }

            create_response = requests.post('http://127.0.0.3:8003/products/create', headers=headers, json=product_data)

            if create_response.status_code == 201:
                messages.success(request, "Product created successfully!")
            else:
                messages.error(request, "Failed to create product.")

            return HttpResponseRedirect('/shop/')
        else:
            return HttpResponse("You are not authorized to create a product.", status=403)


class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')


class ThankYouView(View):
    def get(self, request):
        return render(request, 'thankyou.html')


class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')


class Product_detail(View):
    def get(self, request, product_id):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return HttpResponseRedirect('/auth/login/')
        context = {
            "products": product
        }
        return render(request, 'product_detail.html', context)
