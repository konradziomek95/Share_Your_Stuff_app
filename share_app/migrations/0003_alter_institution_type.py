# Generated by Django 4.1.2 on 2022-10-11 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share_app', '0002_category_institution_donation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.IntegerField(choices=[(1, 'Fundacja'), (2, 'Organizacja pozarządowa'), (3, 'Zbiórka lokalna')], default=1, max_length=24),
        ),
    ]
