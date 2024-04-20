from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User


def user_directory_path(instance, filename):
    return f"user_{instance.user.id}/{filename}"


class Category(models.Model):
    cid = ShortUUIDField(
        unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefgh12345"
    )
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category")

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        # fmt: off
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
        # fmt: on

    def __str__(self):
        return self.title


class Vendor(models.Model):
    vid = ShortUUIDField(
        unique=True, length=10, max_length=20, prefix="ven", alphabet="abcdefgh12345"
    )
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="user_directory_path")
    description = models.TextField(null=True, blank=True)

    address = models.CharField(max_length=100, default="N/A")
    contact = models.CharField(max_length=100, default="N/A")
    chat_resp_time = models.CharField(max_length=100, default="N/A")
    shipping_on_time = models.CharField(max_length=100, default="N/A")
    authentic_rating = models.CharField(max_length=100, default="N/A")
    days_return = models.CharField(max_length=100, default="N/A")
    warranty_period = models.CharField(max_length=100, default="N/A")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
