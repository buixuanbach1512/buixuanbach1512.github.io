# Generated by Django 4.1.4 on 2022-12-26 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_alter_shippingaddress_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='pro_name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
    ]
