from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect
from sellers.models import Seller
from buyers.models import Buyer

def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            is_seller = request.POST.get('is_seller') == 'on'
            if is_seller:
                Seller.objects.create(user=user)
            else:
                Buyer.objects.create(user=user)
            return redirect('login')

    return render(request, 'user/register.html', {
        'form': form
    })