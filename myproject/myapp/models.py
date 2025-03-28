from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    emailAdress = models.TextField()
    phoneNumber = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name