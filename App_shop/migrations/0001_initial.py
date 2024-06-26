# Generated by Django 5.0.1 on 2024-04-30 05:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catagory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=264)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Catagories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mainimage', models.ImageField(upload_to='products')),
                ('name', models.CharField(max_length=264)),
                ('preview_text', models.TextField(max_length=264, verbose_name='Preview Text')),
                ('detail_text', models.TextField(max_length=1000, verbose_name='Description')),
                ('price', models.FloatField()),
                ('old_price', models.FloatField(default=0.0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('catagory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catagory', to='App_shop.catagory')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
