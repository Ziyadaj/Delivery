import datetime
from django import forms
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import User, Package, RetailCenter, TransportationEvent, Location, Truck, Plane, Airport, Customer, TransportedBy, Warehouse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.mail import send_mail,BadHeaderError


categories = ['Regular', 'Liquid', 'Fragile', 'Chemical', 'Other']
status = ['In Transit', 'Delivered', 'Delayed', 'Lost', 'Damaged']
dimensions = ['Small', 'Medium', 'Large', 'Extra Large']
loc_type = ['Trucks', 'Airport', 'Warehouse', 'Plane']
event_type = ['Air', 'Ground', 'Sea']
class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['recipient','weight', 'destination', 'dimensions', 'insurance_amount', 'status', 'category', 'value', 'final_delivery_date']
        widgets = {
            'recipient': forms.Select(choices=[(user, user) for user in User.objects.all()], attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'dimensions': forms.Select(choices=[(dimension, dimension) for dimension in dimensions], attrs={'class': 'form-control'}),
            'insurance_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(choices=[(status, status) for status in status], attrs={'class': 'form-control'}),   
            'category': forms.Select(choices=[(category, category) for category in categories], attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control'}),
            'final_delivery_date': forms.DateInput(attrs={'class': 'form-control'}),
        }
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['city']
        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }
class LocationTypeForm(forms.Form):
    type = forms.ChoiceField(choices=[(type, type) for type in loc_type])
class TransportationEventForm(forms.ModelForm):
    class Meta:
        model = TransportationEvent
        fields = ['type', 'delivery_route']
        widgets = {
            'type': forms.Select(choices=[(type, type) for type in event_type], attrs={'class': 'form-control'}),
            'delivery_route': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RetailCenterForm(forms.ModelForm):
    class Meta:
        model = RetailCenter
        fields = ['address', 'type']
        widgets = {
            'type': forms.Select(choices=[(type, type) for type in ['Retail', 'Distribution']], attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ReportForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=[(status, status) for status in status], widget=forms.Select(attrs={'class': 'form-control'}))
    category = forms.ChoiceField(choices=[(category, category) for category in categories], widget=forms.Select(attrs={'class': 'form-control'}))

def index(request):
    return render(request, 'Delivery/index.html')

#Adminstration/Employee functions

#add/remove/edit package
@login_required
def packages(request): 
    if (not request.user.is_staff):
        #get sent package for user by user id
        packages = Package.objects.filter(user_id=request.user.id)
        #get received package for user by recipient name
        package = Package.objects.filter(recipient=request.user.username)
        return render(request, "Delivery/packages.html", {
            "packages": packages,
            "package": package,
            "isCustomer": True,
            "empty": not packages.exists(),
            "delivered": packages.filter(status="Delivered").exists(),
        })

    packages = Package.objects.all()
    form = PackageForm()
    if request.method == "POST": 
        if form.is_valid():
            #create package
            package = form.save(commit=False)
            package.save()
            #success message
            if (Package.objects.filter(pk=package.id).exists()):
                messages.success(request, 'Form submission successful')
            return HttpResponseRedirect(reverse("packages"))            
        else:
            return render(request, "Delivery/packages.html", {
                "form": form,
                "packages": packages
            })
    return render(request, "Delivery/packages.html", {
        "form": form,
        "packages": packages
    })
def package(request, id):
    package = Package.objects.get(pk=id)
    form1 = PackageForm(request.POST or None, instance=package)
    form2 = LocationForm(request.POST)
    form3 = LocationTypeForm(request.POST)
    # form4 = RetailCenterForm(request.POST)
    form4 = TransportationEventForm(request.POST)
    if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
        form1.save()
        #create location
        form2.save()
        #create package
        package = form1.save(commit=False)
        package.save()
        #create transportation event
        form4.save()
        #create retail center
        # form4.save()
        #create location type
        location_type = form3.save(commit=False)
        if (location_type.type == 'Plane'):
            plane = Plane.objects.create(flight_number="", location=Location.objects.get(city=form2.cleaned_data['city']))
            plane.save()
        elif (location_type.type == 'Truck'):
            truck = Truck.objects.create(truck_number=1, location=Location.objects.get(city=form2.cleaned_data['city']))
            truck.save()
        elif (location_type.type == 'Airport'):
            airport = Airport.objects.create(airport_code="",address=form2.cleaned_data['city'])
            airport.save()
        elif (location_type.type == 'Warehouse'):
            warehouse = Warehouse.objects.create(warehouse_address="",address=form2.cleaned_data['city'])
            warehouse.save()
        location_type.save()
        messages.success(request, 'Package updated successfully')
        return HttpResponseRedirect(reverse("packages"))
    return render(request, "Delivery/package.html", {
        "package": package,
        "form1": PackageForm(instance=package),
        "form2": form2,
        "form3": form3,
        "form4": form4
    })
@login_required
@staff_member_required
@csrf_exempt
def delete(request, id):
    # delete either a package or a user
    if (Package.objects.filter(pk=id).exists()):
        package = Package.objects.get(pk=id)
        package.delete()
        messages.success(request, 'Package deleted successfully')

    elif (User.objects.filter(pk=id).exists()):
        user = User.objects.get(pk=id)
        user.delete()
        messages.success(request, 'User deleted successfully')

    return HttpResponseRedirect(reverse("packages"))
    
#add/remove/edit user

@staff_member_required
def users(request):
    users = User.objects.all()
    form = UserForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            if (User.objects.filter(pk=user.id).exists()):
                messages.success(request, 'Form submission successful')
            return HttpResponseRedirect(reverse("users"))
        else:
            return render(request, 'Delivery/users.html', {
                "form": form,
                "users": users
            })
    return render(request, 'Delivery/users.html', {
        "users": users,
        "form": form
    })
# Edit user info

def user(request, id):
    user = User.objects.get(pk=id)
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        messages.success(request, 'User updated successfully')
        return HttpResponseRedirect(reverse("user", args=(user.id,)))
    return render(request, 'Delivery/user.html', {
        "user": user,
        "form": UserForm(instance=user)
    })
# Email notification
@staff_member_required
def send_email(request):
    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('from_email', '')
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ['admin@example.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('index')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')

def reports(request):
    packages = Package.objects.all()
    #querys
    #List all lost/delayed/delivered packages between two dates
    packages = Package.objects.filter(status='delivered', final_delivery_date__range=['2020-01-01', '2020-12-31'])
    #List the total number of package types (Regular, Fragile, Liquid, Chemical ) that have been sent between two dates.
    packages = Package.objects.filter(category='Regular', final_delivery_date__range=['2020-01-01', '2020-12-31'])
    #Package Delivery Tracking based on categories, locations and status. For example, list all fragile packages currently in transit at Riyadh.
    packages = Package.objects.filter(category='Fragile', status='in transit', location=1)
    #List all packages information either sent or received by a particular customer.
    # packages = Package.objects.filter(user_id=1)
    return render(request, 'Delivery/reports.html', {'packages': packages})

# Trace back packages
def trace(request):
    return render(request, 'Delivery/trace.html')

# Customer functions

#get user package
def get_user_package(request):
    #get user 
    user = User.objects.get(username=request.user)
    package = Package.objects.get(user=user)
    return render(request, 'Delivery/package.html', {'package': package})
#send package
def send_package(request):
    form = PackageForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            package = form.save(commit=False)
            package.user = request.user
            package.save()
            if (Package.objects.filter(pk=package.id).exists()):
                messages.success(request, 'Form submission successful')
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, 'Delivery/send_package.html', {
                "form": form
            })
    return render(request, 'Delivery/send_package.html', {
        "form": form
    })

#payment
@csrf_exempt
@login_required
def payment(request, id):
    #recieve payment
    #and update package status
    package = Package.objects.get(pk=id)
    package.status = 'Delivered'
    package.save()
    return HttpResponseRedirect(reverse("packages"))

#General functions

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "Delivery/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "Delivery/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_customer(request):
    if request.method == "POST":
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "Delivery/register_customer.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "Delivery/register_customer.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Delivery/register_customer.html")

def register_employee(request):
    if request.method == "POST":
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "Delivery/register_employee.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.is_staff = True
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "Delivery/register_employee.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Delivery/register_employee.html")
def menu(request):
    return render(request, 'Delivery/menu.html')