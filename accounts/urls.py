from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('product/', views.product, name='product'),
    path('customer/<int:pk>/', views.customer, name='customer'),
    path('create_order/<int:pk>', views.create_order, name="create"),
    path('update_order/<int:pk>', views.update_order, name="update"),
    path('delete_order/<int:pk>', views.delete_order, name="delete"),
    path('register', views.register, name="register"),
    path('login', views.loginPage, name="login"),
    path('logout', views.logoutUser, name="logout")

]