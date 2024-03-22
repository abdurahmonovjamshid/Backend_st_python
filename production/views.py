from django.dispatch import receiver
from rest_framework import viewsets
from django.db.models.signals import post_save
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from .models import Product, Material, ProductMaterial, Warehouse, ProductionRequest, ReqeustMaterials
from .serializers import (ProductSerializer, MaterialSerializer, ProductMaterialSerializer,
                          WarehouseSerializer, ProductDeteilSerializer,
                          ProductionRequestSerializer, ReqeustMaterialsSerializer)
from django.db.models import Case, F, FloatField, Sum, Value, When
from django.db.models import Q


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

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)


class ProductionRequestViewSet(viewsets.ModelViewSet):
    queryset = ProductionRequest.objects.all()
    serializer_class = ProductionRequestSerializer

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)


@receiver(post_save, sender=ProductionRequest)
def production_save(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        pr_materials = ProductMaterial.objects.filter(product=product)
        for pr_material in pr_materials:
            warehouses_per_m = Warehouse.objects.annotate(
                busy_qty=Sum('reqeustmaterials__qty'),
                calculated_remainder=Case(
                    When(busy_qty__isnull=True, then=F('remainder')),
                    default=F('remainder') - F('busy_qty'),
                    output_field=FloatField()
                )
            ).filter(
                Q(calculated_remainder__gt=0) & Q(
                    material=pr_material.material)
            )
            quantity_needed = pr_material.quantity * instance.quantity
            material_name = pr_material.material.name
            for warehouse_per_m in warehouses_per_m:
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


@receiver(post_save, sender=Warehouse)
def production_save(sender, instance, created, **kwargs):
    needed_requests = ReqeustMaterials.objects.filter(
        Q(material_name=instance.material.name) & Q(warehouse=None))
    for request in needed_requests:
        if request.qty < instance.calculate_remainder:
            request.warehouse = instance
            request.save()
        elif instance.calculate_remainder > 0:
            ReqeustMaterials.objects.create(
                production_request=request.production_request,
                warehouse=None,
                material_name=request.material_name,
                qty=request.qty-instance.calculate_remainder
            )
            request.warehouse = instance
            request.qty = instance.calculate_remainder
            request.save()
