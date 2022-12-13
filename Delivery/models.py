from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

# Customer model
class Customer(models.Model):
    pass
# Package model
class Package(models.Model):
    #primary key
    id = models.AutoField(primary_key=True)
    weight = models.FloatField()
    destination = models.CharField(max_length=100)
    dimensions = models.CharField(max_length=100, default='Small')
    insurance_amount = models.FloatField()
    status = models.CharField(max_length=100, default='In Transit')
    category = models.CharField(max_length=100, default='Regular')
    value = models.FloatField(default=0)
    final_delivery_date = models.DateField()

    #derived attributes
    @property
    def payment(self):
        return self.value * (self.weight * 0.1)
    
    #string representation
    def __str__(self):
        return f"{self.package_number}: {self.weight} {self.destination} {self.dimensions} {self.insurance_amount} {self.status} {self.category} {self.value} {self.final_delivery_date}"

# Retail model
class RetailCenter(models.Model):
    #primary key
    retail_center_number = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    #foreign key
    package_number = models.ForeignKey(Package, on_delete=models.CASCADE, null=True)

# Transportation event model
class TransportationEvent(models.Model):
    #primary key
    schedule_number = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)
    deivery_route = models.CharField(max_length=100)

# Transported By relationship model
class TransportedBy(models.Model):
    #foreign key
    package_number = models.ForeignKey(Package, on_delete=models.CASCADE, null=True)
    schedule_number = models.ForeignKey(TransportationEvent, on_delete=models.CASCADE, null=True)

# Locations model
class Location(models.Model):
    #primary key
    location_number = models.AutoField(primary_key=True, default=1)
    #foreign key
    #one to many
    package = models.ForeignKey(Package, on_delete=models.CASCADE)

# Trucks part of Location model
class Truck(models.Model):
    #primary key
    truck_number = models.AutoField(primary_key=True, default=1)
    #foreign key
    #one to many
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
# Planes part of Location model
class Plane(models.Model):
    #primary key
    flight_number = models.AutoField(primary_key=True, default=123)
    #foreign key
    #one to many
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
# Airports part of Location model
class Airport(models.Model):
    #primary key
    airport_code = models.CharField(max_length=100, primary_key=True, default='ABC')
    #foreign key
    #one to many
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
# Warehouse part of Location model
class Warehouse(models.Model):
    #primary key
    warehouse_address = models.CharField(max_length=100, primary_key=True, default='123 Main St')
    #foreign key
    #one to many
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
