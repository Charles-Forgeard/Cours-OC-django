from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Band(models.Model):

    class Genre(models.TextChoices):
        HIP_HOP = 'HH'
        SYNTH_POP = 'SP'
        ALTERNATIVE_ROCK = 'AR'

    def __str__(self):
        return f'{self.name}'

    name = models.fields.CharField(max_length=100)
    genre = models.fields.CharField(default='',choices=Genre.choices,max_length=5)
    biography = models.fields.CharField(default='', max_length=1000)
    year_formed = models.fields.IntegerField(
        default=0,
        validators=[MinValueValidator(1900), MaxValueValidator(2023)]
    )
    is_active = models.fields.BooleanField(default=True)
    official_page = models.fields.URLField(null=True, blank=True)

class Listing(models.Model):

    class Type(models.TextChoices):
        RECORDS = 'RE'
        CLOTHING = 'CL'
        POSTERS = 'PO'
        MISCELLANEOUS = 'MI'

    band = models.ForeignKey(Band, null=True, on_delete=models.SET_NULL)
    description = models.fields.CharField(max_length=1000)
    sold = models.fields.BooleanField(default=False)
    year = models.fields.IntegerField(
        default=0,
        validators=[MaxValueValidator(2023)]
    )
    type = models.fields.CharField(default='',choices=Type.choices,max_length=5)
