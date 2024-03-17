from django.db import models


class Material(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.FloatField()

    def __str__(self):
        return f"{self.product.name} - {self.material.name}"


class Warehouse(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    remainder = models.FloatField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.material.name

    @property
    def calculate_remainder(self):
        instances = self.reqeustmaterials_set.all()
        busy_qty = 0
        for instance in instances:
            busy_qty += instance.qty
        return self.remainder - busy_qty


class ProductionRequest(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()


class ReqeustMaterials(models.Model):
    production_request = models.ForeignKey(
        ProductionRequest, on_delete=models.CASCADE, related_name='materials')
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, null=True)
    material_name = models.CharField(max_length=100)
    qty = models.FloatField(null=True, blank=True)
