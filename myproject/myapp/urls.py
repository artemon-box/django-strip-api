from django.urls import path

from .views import (
    ItemDetailApiView,
    StripeSessionIdApiView,
    payment_completed,
    payment_canceled,
)

app_name = "myapp"
urlpatterns = [
    path("completed/", payment_completed, name="completed"),
    path("canceled/", payment_canceled, name="canceled"),
    path("item/<int:pk>/", ItemDetailApiView.as_view(), name="item_detail"),
    path("buy/<int:pk>/", StripeSessionIdApiView.as_view(), name="stripe_session_id"),
]
