from rest_framework import serializers
from .models import (Product, Material, ProductMaterial,
                     Warehouse, ProductionRequest, ReqeustMaterials)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class ProductDeteilSerializer(serializers.ModelSerializer):
    material = serializers.CharField(read_only=True)

    class Meta:
        model = ProductMaterial
        fields = '__all__'


class ProductMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMaterial
        fields = ['id', 'product', 'material', 'quantity']


class WarehouseSerializer(serializers.ModelSerializer):
    material_name = serializers.SerializerMethodField()

    class Meta:
        model = Warehouse
        fields = ['id', 'material', 'material_name', 'remainder',
                  'price']

    def get_material_name(self, obj):
        return obj.material.name if obj.material else None


class ReqeustMaterialsSerializer(serializers.ModelSerializer):
    warehouse_id = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = ReqeustMaterials
        fields = ['warehouse_id', 'material_name', 'qty', 'price']

    def get_warehouse_id(self, obj):
        return obj.warehouse.id if obj.warehouse else None

    def get_price(self, obj):
        return obj.warehouse.price if obj.warehouse else None


class ProductionRequestSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_materials = serializers.SerializerMethodField()

    class Meta:
        model = ProductionRequest
        fields = ['id', 'product', 'product_name',
                  'quantity', 'product_materials']

    def get_product_materials(self, obj):
        serializer = ReqeustMaterialsSerializer(
            obj.materials.all(), many=True, read_only=True)
        return serializer.data

    def get_product_name(self, obj):
        return obj.product.name if obj.product else None
