from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField


STATUS_CHOICE = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "In Review"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

RATING = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)


def user_directory_path(instance, filename):
    return f"user_{instance.user.id}/{filename}"


class Category(models.Model):
    cid = ShortUUIDField(
        unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefgh12345"
    )
    title = models.CharField(max_length=100, default="N/A")
    image = models.ImageField(upload_to="category", default="category.jpg")

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        # fmt: off
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
        # fmt: on

    def __str__(self):
        return self.title


class Tags(models.Model):
    pass


class Vendor(models.Model):
    vid = ShortUUIDField(
        unique=True, length=10, max_length=20, prefix="ven", alphabet="abcdefgh12345"
    )
    title = models.CharField(max_length=100, default="N/A")
    image = models.ImageField(upload_to="user_directory_path", default="vendor.jpg")
    cover_image = models.ImageField(
        upload_to="user_directory_path", default="vendor.jpg"
    )
    # description = models.TextField(null=True, blank=True, default="N/A")
    description = RichTextUploadingField(null=True, blank=True, default="N/A")

    address = models.CharField(max_length=100, default="N/A")
    contact = models.CharField(max_length=100, default="N/A")
    chat_resp_time = models.CharField(max_length=100, default="N/A")
    shipping_on_time = models.CharField(max_length=100, default="N/A")
    authentic_rating = models.CharField(max_length=100, default="N/A")
    days_return = models.CharField(max_length=100, default="N/A")
    warranty_period = models.CharField(max_length=100, default="N/A")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        # fmt: off
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
        # fmt: on

    def __str__(self):
        return self.title


class Product(models.Model):
    pid = ShortUUIDField(
        unique=True, length=10, max_length=20, alphabet="abcdefgh12345"
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="category"
    )
    vendor = models.ForeignKey(
        Vendor, on_delete=models.SET_NULL, null=True, related_name="vendor"
    )

    title = models.CharField(max_length=100, default="N/A")
    image = models.ImageField(upload_to="user_directory_path", default="product.jpg")
    # description = models.TextField(null=True, blank=True, default="N/A")
    description = RichTextUploadingField(null=True, blank=True, default="N/A")

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # specifications = models.TextField(null=True, blank=True, default="N/A")
    specifications = RichTextUploadingField(null=True, blank=True, default="N/A")
    type = models.CharField(max_length=100, default="N/A", null=True, blank=True)
    stock_count = models.CharField(max_length=100, default="N/A", null=True, blank=True)
    life = models.CharField(max_length=100, default="N/A", null=True, blank=True)
    mfd = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    tags = TaggableManager(blank=True)

    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    product_status = models.CharField(
        choices=STATUS, max_length=10, default="in_review"
    )

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    sku = ShortUUIDField(
        unique=True, length=4, max_length=10, prefix="sku", alphabet="1234567890"
    )

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        # fmt: off
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
        # fmt: on

    def __str__(self):
        return self.title

    def get_percentage(self):
        new_price = (self.old_price - self.price) / self.old_price * 100
        return new_price


class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(
        Product, related_name="p_images", on_delete=models.SET_NULL, null=True
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"


class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(
        choices=STATUS_CHOICE, max_length=30, default="processing"
    )

    class Meta:
        verbose_name_plural = "Cart Order"


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_img(self):
        # fmt: off
        return mark_safe(f'<img src="/media/{self.image}" width="50" height="50" />')
        # fmt: on


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name="reviews"
    )
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return self.product.title

    def get_rating(self):
        return


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlists"

    def __str__(self):
        return self.product.title


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"
