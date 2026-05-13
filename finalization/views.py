from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from bids.models import Bid
from .forms import ContactInformationForm, PaymentForm

@login_required
def finalize_contact(request, bid_id):
    bid = get_object_or_404(
        Bid,
        id=bid_id,
        buyer=request.user.buyer,
        status="accepted"
    )

    session_key = f"finalization_{bid.id}_contact"
    saved_data = request.session.get(session_key, None)

    if request.method == "POST":
        form = ContactInformationForm(request.POST)
        if form.is_valid():
            request.session[session_key] = form.cleaned_data
            return redirect("finalize-payment", bid_id=bid.id)
    else:
        form = ContactInformationForm(initial=saved_data)

    return render(request, "finalization/contact.html", {
        "bid": bid,
        "form": form
    })

@login_required
def finalize_payment(request, bid_id):
    bid = get_object_or_404(
        Bid,
        id=bid_id,
        buyer=request.user.buyer,
        status="accepted"
    )

    contact_key = f"finalization_{bid.id}_contact"
    payment_key = f"finalization_{bid.id}_payment"

    contact_data = request.session.get(contact_key)

    if not contact_data:
        return redirect("finalize-contact", bid_id=bid.id)

    saved_payment = request.session.get(payment_key, None)

    if request.method == "POST":
        form = PaymentForm(request.POST)

        if form.is_valid():
            request.session[payment_key] = form.cleaned_data
            return redirect("finalize-review", bid_id=bid.id)

    else:
        form = PaymentForm(initial=saved_payment)

    return render(request, "finalization/payment.html", {
        "bid": bid,
        "form": form,
        "contact": contact_data,
    })


@login_required
def finalize_review(request, bid_id):
    bid = get_object_or_404(
        Bid,
        id=bid_id,
        buyer=request.user.buyer,
        status="accepted"
    )

    contact_key = f"finalization_{bid.id}_contact"
    payment_key = f"finalization_{bid.id}_payment"

    contact = request.session.get(contact_key)
    payment = request.session.get(payment_key)

    if not contact:
        return redirect("finalize-contact", bid_id=bid.id)

    if not payment:
        return redirect("finalize-payment", bid_id=bid.id)

    if request.method == "POST":
        bid.status = "finalized"
        bid.save()

        return redirect("finalize-confirmation", bid_id=bid.id)

    return render(request, "finalization/review.html", {
        "bid": bid,
        "contact": contact,
        "payment": payment,
    })

@login_required
def finalize_confirmation(request, bid_id):
    bid = get_object_or_404(
        Bid,
        id=bid_id,
        buyer=request.user.buyer,
        status="finalized"
    )

    return render(request, "finalization/confirmation.html", {
        "bid": bid,
    })