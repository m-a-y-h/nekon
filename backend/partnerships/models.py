from django.db import models

class Partner(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    date_joined = models.DateField(auto_now_add=True)

class Share(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    percentage = models.FloatField()  # Share percentage
    dividends = models.DecimalField(max_digits=10, decimal_places=2)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
