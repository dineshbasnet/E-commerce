from django.urls import path
from vendor import views

urlpatterns = [
    path("products/", views.vendor_products, name="vendor_products"),
    path("products/add/", views.add_product, name="add_product"),
    path("products/edit/<int:product_id>/", views.edit_product, name="edit_product"),
    path("products/delete/<int:product_id>/", views.delete_product, name="delete_product"),
]
