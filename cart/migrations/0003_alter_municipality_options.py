# Generated by Django 5.1.5 on 2025-01-29 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_district_state_cartproduct_ordered_municipality_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='municipality',
            options={'verbose_name_plural': 'Municipalities'},
        ),
    ]
