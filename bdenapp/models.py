from django.db import models
from django.db.models import Count
from collections import defaultdict
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    CATEGORIES = models.TextChoices('CATEGORIES', 'Apartment Residence Unit')
    name = models.CharField(max_length=15, choices=CATEGORIES)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'categories'

    def __str__(self):
        return f"{self.name}"
    
class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties', null=True, blank=False)
    location = models.CharField(max_length=250)
    owner = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=12, decimal_places=2)
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
    images = models.FileField(upload_to='more_pictures/', null=True, blank=True)

    class Meta:
        db_table = 'more_images'
        verbose_name_plural = 'propertyImages'
        

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.username} - {self.review_text}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_owner = models.BooleanField(default=False)
    is_merchant = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_profile'

    def __str__(self):
        return f"{self.user.username}"
    
class SavedItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    # quantity = models.PositiveIntegerField()
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'purchase'
        ordering = ['purchased_at']

    def __str__(self):
        return f"{self.user.username}"
    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='NGN')
    STAGE = models.TextChoices('STAGE', 'Pending Completed Failed')
    status = models.CharField(max_length=20, choices=STAGE)
    transaction_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payment'
        ordering = ['created_at']
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.currency} ({self.status})"

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