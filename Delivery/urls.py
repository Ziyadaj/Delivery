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
    path("user/<int:id>", views.user, name="user"),
    path("reports", views.reports, name="reports"),
    path("send_package", views.send_package, name="send_package"),

    # jQuery Routes
    path("delete/<int:id>", views.delete, name="delete"),
    path("user/delete/<int:id>", views.delete, name="delete"),
    path("pay/<int:id>", views.payment, name="pay"),

    #API Routes
    path("send_email", views.send_email, name="send_email"),
]