# Generated by Django 3.2.7 on 2021-09-25 20:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cashback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sold_at', models.DateTimeField()),
                ('total', models.FloatField()),
                ('created_at', models.DateTimeField(null=True)),
                ('message', models.CharField(default='Waiting for cashback api response', max_length=255)),
                ('returned_id', models.IntegerField(null=True)),
                ('cashback', models.FloatField(null=True)),
                ('document', models.CharField(max_length=11, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='people.customer')),
                ('products', models.ManyToManyField(to='products.Product')),
            ],
        ),
    ]
