from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import requests
from django.contrib import messages
from django.views import View

class DeliveryView(View):
    def get(self, request):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return HttpResponseRedirect('/auth/login/')

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.get('http://127.0.0.3:8003/deliveries/', headers=headers)
        deliveries = response.json() if response.status_code == 200 else []

        return render(request, 'deliveries.html', {'deliveries': deliveries})

    def post(self, request):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return HttpResponseRedirect('/auth/login/')

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        delivery_data = {
            'order_id': request.POST.get('order_id'),
            'status': request.POST.get('status')
        }

        response = requests.post('http://127.0.0.3:8003/deliveries/', headers=headers, json=delivery_data)

        if response.status_code == 201:
            messages.success(request, "Delivery created successfully!")
        else:
            messages.error(request, "Failed to create delivery.")

        return redirect('/deliveries/')


class DeliveryDetailView(View):
    def get(self, request, delivery_id):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return HttpResponseRedirect('/auth/login/')

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.get(f'http://127.0.0.3:8003/deliveries/{delivery_id}/', headers=headers)
        delivery = response.json() if response.status_code == 200 else None

        if not delivery:
            return HttpResponse("Delivery not found", status=404)

        return render(request, 'delivery_detail.html', {'delivery': delivery})
