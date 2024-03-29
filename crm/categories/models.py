from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return self.name
