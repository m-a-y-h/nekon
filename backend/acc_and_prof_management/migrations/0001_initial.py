# Generated by Django 5.1.1 on 2024-10-14 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_en', models.CharField(max_length=255)),
                ('description_en', models.TextField()),
                ('price_en', models.DecimalField(decimal_places=2, max_digits=10)),
                ('title_fr', models.CharField(max_length=255)),
                ('description_fr', models.TextField()),
                ('price_fr', models.DecimalField(decimal_places=2, max_digits=10)),
                ('calories', models.IntegerField()),
                ('dietary', models.CharField(max_length=255)),
                ('allergens', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='dishes/')),
            ],
        ),
    ]
