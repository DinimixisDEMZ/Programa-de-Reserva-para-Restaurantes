from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class TableStatus(models.IntegerChoices):
    OCCUPIED = 0, 'Ocupada'
    FREE = 1, 'Libre'
    RESERVED = 2, 'Reservada'

class Table(models.Model):
    location = models.CharField(max_length=200, help_text='Ubicación de la mesa (ex:Terraza)')
    number_of_chairs = models.IntegerField(default=5, validators=[MinValueValidator(2),MaxValueValidator(12)], help_text='Número de sillas que tiene la mesa (ex:5)')
    status = models.IntegerField(choices=TableStatus.choices, default=TableStatus.FREE, help_text='Estado actual de la mesa (ex:Ocupada)')
    
    def __str__(self):
        return 'ID:{} Number of chairs:{} Status:{}'.format(self.pk, self.number_of_chairs, self.status)