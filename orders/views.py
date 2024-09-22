from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.contrib import messages
import requests


class OrderView(View):
    def get(self, request):
        access_token = request.COOKIES.get('access_token')

        if not access_token:
            return HttpResponseRedirect('/auth/login/')

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.get('http://127.0.0.3:8003/identify/token/verify', headers=headers)

        if response.status_code == 200:
            # Fetch orders for the user
            orders_response = requests.get('http://127.0.0.3:8003/orders/', headers=headers)
            orders = orders_response.json() if orders_response.status_code == 200 else []
            return render(request, 'orders.html', {'orders': orders})
        else:
            response = HttpResponseRedirect('/auth/login/')
            response.delete_cookie('access_token')
            return response

    def post(self, request):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return HttpResponseRedirect('/auth/login/')

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        order_data = {
            'product_id': request.POST.get('product_id'),
            'quantity': request.POST.get('quantity')
        }

        create_response = requests.post('http://127.0.0.3:8003/orders/', headers=headers, json=order_data)

        if create_response.status_code == 201:
            messages.success(request, "Order created successfully!")
        else:
            messages.error(request, "Failed to create order.")

        return HttpResponseRedirect('/orders/')

    def put(self, request, order_id):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return HttpResponseRedirect('/auth/login/')

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        # Get order data from the request
        order_data = {
            'product_id': request.POST.get('product_id'),
            'quantity': request.POST.get('quantity')
        }

        # Send update request to the API
        update_response = requests.put(f'http://127.0.0.3:8003/orders/{order_id}/', headers=headers, json=order_data)

        if update_response.status_code == 200:
            messages.success(request, "Order updated successfully!")
        else:
            messages.error(request, "Failed to update order.")

        return HttpResponseRedirect('/orders/')

    def delete(self, request, order_id):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return HttpResponseRedirect('/auth/login/')

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        delete_response = requests.delete(f'http://127.0.0.3:8003/orders/{order_id}/', headers=headers)

        if delete_response.status_code == 204:
            messages.success(request, "Order deleted successfully!")
        else:
            messages.error(request, "Failed to delete order.")

        return HttpResponseRedirect('/orders/')
