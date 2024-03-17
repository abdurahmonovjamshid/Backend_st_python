from django.urls import path, include
from rest_framework import routers
from .views import ProductViewSet, MaterialViewSet, ProductMaterialViewSet, WarehouseViewSet, ProductionRequestViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'materials', MaterialViewSet)
router.register(r'product-materials', ProductMaterialViewSet)
router.register(r'warehouses', WarehouseViewSet)
router.register(r'production-request', ProductionRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
