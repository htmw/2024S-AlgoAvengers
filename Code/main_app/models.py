from django.db import models

# Create your models here.

class Areas(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class Plants(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='plants/', null=True, blank=True)

    def __str__(self):
        return self.name

class Soils(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    plant = models.ForeignKey(Plants, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='soils/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.plant}"

class SoilDetails(models.Model):
    soil = models.ForeignKey(Soils, on_delete=models.SET_NULL, null=True)
    area = models.ForeignKey(Areas, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.area} {self.soil}"



    
