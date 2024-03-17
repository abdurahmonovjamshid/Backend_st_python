from django.dispatch import receiver
from rest_framework import viewsets
from django.db.models.signals import post_save
from rest_framework.response import Response
from .models import Product, Material, ProductMaterial, Warehouse, ProductionRequest, ReqeustMaterials
from .serializers import (ProductSerializer, MaterialSerializer, ProductMaterialSerializer,
                          WarehouseSerializer, ProductDeteilSerializer,
                          ProductionRequestSerializer, ReqeustMaterialsSerializer)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        product_materials = instance.productmaterial_set.all()
        product_materials_serializer = ProductDeteilSerializer(
            product_materials, many=True, read_only=True)
        data = serializer.data
        data['product_materials'] = product_materials_serializer.data
        return Response(data)


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class ProductMaterialViewSet(viewsets.ModelViewSet):
    queryset = ProductMaterial.objects.all()
    serializer_class = ProductMaterialSerializer


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class ProductionRequestViewSet(viewsets.ModelViewSet):
    queryset = ProductionRequest.objects.all()
    serializer_class = ProductionRequestSerializer


@receiver(post_save, sender=ProductionRequest)
def production_save(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        pr_materials = ProductMaterial.objects.filter(product=product)
        for pr_material in pr_materials:
            warehouses_per_m = Warehouse.objects.filter(
                material=pr_material.material)

            quantity_needed = pr_material.quantity * instance.quantity
            for warehouse_per_m in warehouses_per_m:
                material_name = warehouse_per_m.material.name
                available_quantity = warehouse_per_m.calculate_remainder

                if quantity_needed <= available_quantity:
                    qty = quantity_needed
                    quantity_needed = 0
                    ReqeustMaterials.objects.create(
                        production_request=instance,
                        warehouse=warehouse_per_m,
                        material_name=material_name,
                        qty=qty
                    )
                    break
                elif available_quantity > 0:
                    qty = available_quantity
                    quantity_needed -= qty
                    ReqeustMaterials.objects.create(
                        production_request=instance,
                        material_name=material_name,
                        warehouse=warehouse_per_m,
                        qty=qty
                    )
            if quantity_needed > 0:
                ReqeustMaterials.objects.create(
                    production_request=instance,
                    warehouse=None,
                    material_name=material_name,
                    qty=quantity_needed
                )
