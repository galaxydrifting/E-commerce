from core.models import (
    # Product,
    Category,
    Vendor,
    # CartOrder,
    # CartOrderItems,
    # ProductImages,
    # ProductReview,
    # Wishlist,
    Address,
)


def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()

    try:
        address = Address.objects.get(user=request.user)
    except Exception:
        address = None

    return {
        "categories": categories,
        "address": address,
        "vendors": vendors,
    }
