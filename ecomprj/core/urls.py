from django.urls import path
from core import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("products/", views.product_list_view, name="product-list"),
    path("product/<pid>", views.product_detail_view, name="product-detail"),
    path("category/", views.category_list_view, name="category_list"),
    path(
        "category/<cid>", views.category_product_list_view, name="category-product-list"
    ),
    path("vendors/", views.vendor_list_view, name="vendor-list"),
    path("vendors/<vid>", views.vendor_detail_view, name="vendor-detail"),
    path("products/tag/<slug:tag_slug>", views.tag_list, name="tag-list"),
]
