from decimal import Decimal

import stripe
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from rest_framework.generics import RetrieveAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Item


stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


class ItemDetailApiView(RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "myapp/item_detail.html"

    def get(self, request, *args, **kwargs):
        item = Item.objects.get(pk=kwargs["pk"])
        return Response({"item": item, "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLISHABLE_KEY})


class StripeSessionIdApiView(APIView):
    def get(self, request, *args, **kwargs):
        item = Item.objects.get(pk=kwargs["pk"])
        success_url = request.build_absolute_uri(reverse("myapp:completed"))
        cancel_url = request.build_absolute_uri(reverse("myapp:canceled"))
        session_data = {
            "mode": "payment",
            "success_url": success_url,
            "cancel_url": cancel_url,
            "line_items": [
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": item.name,
                        },
                        "unit_amount": int(item.price * Decimal("100")),
                    },
                    "quantity": 1,
                }
            ],
        }
        session = stripe.checkout.Session.create(**session_data)
        return Response({"session_id": session.id})


def payment_completed(request):
    return render(request, "myapp/completed.html")


def payment_canceled(request):
    return render(request, "myapp/canceled.html")
