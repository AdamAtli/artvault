from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect
from sellers.models import Seller
from buyers.models import Buyer

def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            is_seller = request.POST.get('is_seller') == 'on'

            if is_seller:
                seller_type = request.POST.get('seller_type')
                Seller.objects.create(user=user, seller_type=seller_type)
                login(request, user)
                return redirect('edit-seller-profile')
            else:
                Buyer.objects.create(user=user)
                login(request, user)
                return redirect('artworks-index')

    return render(request, 'user/register.html', {
        'form': form
    })