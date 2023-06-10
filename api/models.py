from django.db import models
# Create your models here.

class Group(models.Model):
    name  = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Device(models.Model):
    name  = models.CharField(max_length=200)
    ip  = models.CharField(max_length=200)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=0)
    status = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.name} - {self.group.name}"