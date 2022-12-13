from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register/customer", views.register_customer, name="register_customer"),
    path("register/employee", views.register_employee, name="register_employee"),
    path("menu", views.menu, name="menu"),
    path("packages", views.packages, name="packages"),
    path("package/<int:id>", views.package, name="package"),
    path("users", views.users, name="users"),

    # jQuery Routes
    path("delete/<int:id>", views.delete, name="delete"),
]