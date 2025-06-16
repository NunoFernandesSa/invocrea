from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, QuoteViewSet, InvoiceViewSet, LineItemViewSet

router = DefaultRouter()
router.register(r"clients", ClientViewSet)
router.register(r"quotes", QuoteViewSet)
router.register(r"invoices", InvoiceViewSet)
router.register(r"line-items", LineItemViewSet)

urlpatterns = router.urls
urlPaterns = [
    path("", ClientViewSet, name="clients"),
]
