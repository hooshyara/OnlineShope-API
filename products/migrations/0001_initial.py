# Generated by Django 4.2.5 on 2024-01-16 12:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.PositiveIntegerField(default=30)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField(null=True)),
                ('cover', models.ImageField(null=True, upload_to='products/')),
                ('star', models.CharField(choices=[('1', 'یک ستاره'), ('2', 'دو ستاره'), ('3', 'سه ستاره'), ('4', 'چهار ستاره'), ('5', 'پنج ستاره ')], max_length=100, null=True)),
                ('price', models.PositiveBigIntegerField(default=0)),
                ('second_price', models.PositiveBigIntegerField(default=0)),
                ('inventory', models.IntegerField(default=0, null=True)),
                ('active', models.BooleanField(default=True)),
                ('discouont', models.PositiveIntegerField(default=0, null=True)),
                ('Datetime_create', models.DateTimeField(auto_now_add=True)),
                ('Datetime_modified', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.category')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comparison',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.CharField(choices=[('1', 'یک ستاره'), ('2', 'دو ستاره'), ('3', 'سه ستاره'), ('4', 'چهار ستاره'), ('5', 'پنج ستاره ')], max_length=100, null=True)),
                ('text', models.TextField(null=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='products.products')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
