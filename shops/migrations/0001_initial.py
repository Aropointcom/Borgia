# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-04 14:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('finances', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_available_for_sale', models.BooleanField(default=False)),
                ('is_available_for_borrowing', models.BooleanField(default=False)),
                ('peremption_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='SingleProductFromContainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finances.Purchase')),
            ],
        ),
        migrations.CreateModel(
            name='Tap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Container',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shops.Product')),
                ('initial_quantity', models.FloatField()),
                ('estimated_remaining_quantity', models.FloatField(blank=True, null=True)),
                ('is_empty', models.BooleanField(default=False)),
                ('opening_date', models.DateField(blank=True, null=True)),
                ('removing_date', models.DateField(blank=True, null=True)),
                ('is_returnable', models.BooleanField()),
                ('value_when_returned', models.FloatField(blank=True, null=True)),
                ('return_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=('shops.product',),
        ),
        migrations.CreateModel(
            name='ProductUnit',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shops.Product')),
                ('price', models.FloatField()),
                ('unit', models.CharField(max_length=10)),
                ('type', models.CharField(choices=[('keg', 'Fût'), ('other', 'Autre')], max_length=255)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=('shops.product',),
        ),
        migrations.CreateModel(
            name='SingleProduct',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shops.Product')),
                ('is_sold', models.BooleanField(default=False)),
                ('price', models.FloatField()),
                ('purchase', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='finances.Purchase')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=('shops.product',),
        ),
        migrations.AddField(
            model_name='product',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shops.Shop'),
        ),
        migrations.AddField(
            model_name='tap',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shops.Container'),
        ),
        migrations.AddField(
            model_name='singleproductfromcontainer',
            name='container',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.Container'),
        ),
        migrations.AddField(
            model_name='container',
            name='product_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.ProductUnit'),
        ),
    ]