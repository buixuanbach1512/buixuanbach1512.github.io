# Generated by Django 4.1.4 on 2022-12-26 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_alter_category_cat_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='cat_status',
            field=models.BooleanField(default=False),
        ),
    ]
