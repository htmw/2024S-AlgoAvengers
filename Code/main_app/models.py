from django.db import models
from django.contrib.auth.models import User

class LeafDiseaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.TextField()
    disease_name = models.CharField(max_length=100)
    description = models.TextField()
    symptoms = models.TextField()
    prevent = models.TextField()
    supplement_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.disease_name}"


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



    
