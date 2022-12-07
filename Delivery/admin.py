from django.contrib import admin
from .models import User, Package, RetailCenter, TransportedBy, TransportationEvent, Location, Truck, Plane, Airport, Customer

# Register your models here.
admin.site.register(User)
admin.site.register(Package)
admin.site.register(RetailCenter)
admin.site.register(TransportedBy)
admin.site.register(TransportationEvent)
admin.site.register(Location)
admin.site.register(Truck)
admin.site.register(Plane)
admin.site.register(Airport)
admin.site.register(Customer)
