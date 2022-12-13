from django import forms
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import User, Package, RetailCenter, TransportationEvent, Location, Truck, Plane, Airport, Customer, TransportedBy
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

categories = ['Regular', 'Liquid', 'Fragile', 'Chemical', 'Other']
status = ['In Transit', 'Delivered', 'Delayed', 'Lost', 'Damaged']
dimensions = ['Small', 'Medium', 'Large', 'Extra Large']
class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['weight', 'destination', 'dimensions', 'insurance_amount', 'status', 'category', 'value', 'final_delivery_date']
        widgets = {
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'dimensions': forms.Select(choices=[(dimension, dimension) for dimension in dimensions], attrs={'class': 'form-control'}),
            'insurance_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(choices=[(status, status) for status in status], attrs={'class': 'form-control'}),   
            'category': forms.Select(choices=[(category, category) for category in categories], attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control'}),
            'final_delivery_date': forms.DateInput(attrs={'class': 'form-control'}),
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


def index(request):
    return render(request, 'Delivery/index.html')

#Adminstration/Employee functions

#add/remove/edit package
@login_required
@staff_member_required
def packages(request): 
    form = PackageForm(request.POST)
    packages = Package.objects.all()
    if request.method == "POST": 
        if form.is_valid():
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
    form = PackageForm(request.POST or None, instance=package)
    if form.is_valid():
        form.save()
        messages.success(request, 'Package updated successfully')
        return HttpResponseRedirect(reverse("packages"))
    return render(request, "Delivery/package.html", {
        "package": package,
        "form": PackageForm(instance=package)
    })
@login_required
@staff_member_required
@csrf_exempt
def delete(request, id):
    package = Package.objects.get(pk=id)
    package.delete()
    return HttpResponseRedirect(reverse("packages"))
    
#add/remove/edit user

@staff_member_required
def users(request):
    users = User.objects.all()
    form = UserForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            if 'add' in request.POST:
                user = form.save(commit=False)
                user.set_password(user.password)
                user.save()
                if (User.objects.filter(pk=user.id).exists()):
                    messages.success(request, 'Form submission successful')
                return HttpResponseRedirect(reverse("users"))
            if 'edit' in request.POST:
                user = User.objects.get(pk=id)
                form = UserForm(request.POST or None, instance=user)
                form.save()
                messages.success(request, 'User updated successfully')
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

# Email notification
@staff_member_required
def send_notification(request, customer):
    return render(request, 'Delivery/send_notification.html', {
        "customer": customer
    })

def report(request):
    return render(request, 'Delivery/report.html')


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
    return render(request, 'Delivery/send_package.html')

def update_info(request):
    return render(request, 'Delivery/update_info.html')

def payment(request):
    return render(request, 'Delivery/payment.html')
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