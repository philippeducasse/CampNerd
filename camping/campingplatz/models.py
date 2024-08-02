from django.db import models

class Campingplatz(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    customer_number = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name