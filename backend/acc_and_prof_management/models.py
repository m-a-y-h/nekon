from django.db import models

class Dish(models.Model):
    title_en = models.CharField(max_length=255)
    description_en = models.TextField()
    price_en = models.DecimalField(max_digits=10, decimal_places=2)
    calories = models.IntegerField()
    dietary = models.CharField(max_length=255)
    allergens = models.CharField(max_length=255)
    image = models.ImageField(upload_to='dishes/')

    def __str__(self):
        return self.title_en
