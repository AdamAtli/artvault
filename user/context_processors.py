from buyers.models import Buyer
from sellers.models import Seller

def profile_context(request):
    current_buyer = None
    current_seller = None

    if request.user.is_authenticated:
        current_buyer = Buyer.objects.filter(user=request.user).first()
        current_seller = Seller.objects.filter(user=request.user).first()

    return {
        "current_buyer": current_buyer,
        "current_seller": current_seller,
    }