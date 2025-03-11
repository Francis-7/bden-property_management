from django.db import models
from django.db.models import Count
from collections import defaultdict
from django.contrib.auth.models import User

class Category(models.Model):
    CATEGORIES = models.TextChoices('CATEGORIES', 'Apartment Residence Unit')
    name = models.CharField(max_length=15, choices=CATEGORIES)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'categories'

    def __str__(self):
        return f"{self.name}"
    
class Property(models.Model):
    location = models.CharField(max_length=250)
    owner = models.CharField(max_length=150)
    price = models.FloatField()
    propertyType = models.TextChoices('propertyType', 'studio 1-bedroom 2-bedroom 3-bedroom pent-house single-family-home town-house condominium duplex villa luxury-apartment estate-home mansion private-villa pent-house-suite')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    typeChoice = models.CharField(max_length=150, choices=propertyType, default='')
    description = models.CharField(max_length=500)
    isAvailable = models.BooleanField(default=True)
    STATUS = models.TextChoices('STATUS', 'Rent Lease Sale')
    picture = models.ImageField(upload_to="images/")
    uploaded = models.DateField(auto_now_add=True)
    isPeerToPeer = models.BooleanField(default=False)
    provision = models.CharField(max_length=10, choices=STATUS, default='rent')

    class Meta:
        db_table = 'property'
        verbose_name_plural = 'properties'
        ordering = ['location']

    def __str__(self):
        return f'{self.typeChoice}, {self.owner} {self.location}'


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='more_pictures/', null=True, blank=True)

    class Meta:
        db_table = 'more_images'
        verbose_name_plural = 'propertyImages'
        

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review'

    def __str__(self):
        return f"{self.user.username} - {self.review_text}"

def group_and_sort_by_first_word():
    # fetch all objects
    objects = Property.objects.all()
    groups = defaultdict(int)

    for obj in objects:
        # extract the first word before the first comma
        first_word = obj.location.split(',', 1)[0]
        groups[first_word] += 1

    # sort the groups by the first word
    sorted_groups = dict(sorted(groups.items()))
    return sorted_groups