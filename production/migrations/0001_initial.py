# Generated by Django 5.0.3 on 2024-03-17 11:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProductionRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production.material')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production.product')),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remainder', models.FloatField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production.material')),
            ],
        ),
        migrations.CreateModel(
            name='ReqeustMaterials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_name', models.CharField(max_length=100)),
                ('qty', models.FloatField(blank=True, null=True)),
                ('production_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='production.productionrequest')),
                ('warehouse', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='production.warehouse')),
            ],
        ),
    ]
