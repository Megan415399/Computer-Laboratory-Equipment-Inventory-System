from django.db import models

class Equipment(models.Model):
    equipment_id = models.AutoField(primary_key=True)
    equipment_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    condition = models.CharField(max_length=100)  
    status = models.CharField(max_length=100)     
    location = models.CharField(max_length=100)   

    def __str__(self):
        return self.equipment_name