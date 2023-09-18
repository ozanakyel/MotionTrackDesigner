from django.db import models

# Create your models here.
from django.db import models

class Camera(models.Model):
    camera_ip = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Rectangle(models.Model):
    xmin = models.IntegerField()
    ymin = models.IntegerField()
    xmax = models.IntegerField()
    ymax = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rectangle {self.id}"