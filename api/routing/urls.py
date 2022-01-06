from django.urls import path
from routing.views import RoutingAPIView

urlpatterns: list[path] = [path("routing", RoutingAPIView.as_view(), name="routing")]
