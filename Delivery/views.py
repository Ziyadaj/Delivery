from django import forms
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import User, Package, RetailCenter, TransportationEvent, Location, Truck, Plane, Airport, Customer, TransportedBy
from django.contrib.admin.views.decorators import staff_member_required

categories = ['Regular', 'Liquid', 'Fragile', 'Chemical', 'Other']
class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['weight', 'destination', 'dimensions', 'insurance_amount', 'status', 'category', 'value', 'final_delivery_date']
        widgets = {
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'dimensions': forms.TextInput(attrs={'class': 'form-control'}),
            'insurance_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=[(category, category) for category in categories], attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control'}),
            'final_delivery_date': forms.DateInput(attrs={'class': 'form-control'}),
        }



def index(request):
    return render(request, 'Delivery/index.html')

#add/remove/edit package
@login_required
@staff_member_required
def package(request): 
    form = PackageForm(request.POST)
    if request.method == "POST": 
        if form.is_valid():
            package = form.save(commit=False)
            package.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "Delivery/package.html", {
                "form": form
            })
    return render(request, "Delivery/package.html", {
        "form": form
    })
# Edit user info
@staff_member_required
def edit_user(request):
    return render(request, 'Delivery/edit_user.html')
# Email notification
@staff_member_required
def send_notification(request, customer):
    return render(request, 'Delivery/send_notification.html', {
        "customer": customer
    })
# Trace back packages
def trace(request):
    return render(request, 'Delivery/trace.html')

#get user package
def get_user_package(request):
    #get user 
    user = User.objects.get(username=request.user)
    package = Package.objects.get(user=user)
    return render(request, 'Delivery/package.html', {'package': package})

#

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