from django.shortcuts import render, redirect
from django.http import HttpResponse
from listings.models import Band, Listing
from listings.forms import ContactUsForm, BandForm, ListingsForm
# serveur de messagerie fictive de Django.
from django.core.mail import send_mail
# Create your views here.

def band_list(request):
    bands = Band.objects.all()
    return render(request, 
                'listings/band_list.html',
                context={'bands': bands})

def band_detail(request, band_name):
    band_instance = Band.objects.get(name=band_name)
    band_dict = band_instance.__dict__
    return render(request=request,
                  template_name='listings/band_detail.html',
                  context={'band': band_dict, 'band_instance': band_instance})

def band_create(request):
    if request.method == 'POST':
        form = BandForm(request.POST) 
        if form.is_valid():
            band = form.save() # enregistre en base de données puis revoit l'objet
            return redirect('band_detail', band.name)
    else:
        form = BandForm()
    return render(
        request=request,
        template_name='listings/band_create.html',
        context={'form': form}
    )

def band_update(request, band_name):
    band = Band.objects.get(name=band_name)
    if request.method == 'POST':
        form = BandForm(request.POST, instance=band)
        if form.is_valid:
            form.save()
            return redirect('band_detail', band.name)
    else:
        form = BandForm(instance=band)
    return render(
        request=request,
        template_name='listings/band_update.html',
        context={'form': form}
    )

def band_delete(request, band_name):
    band = Band.objects.get(name=band_name)
    if request.method == 'POST':
        band.delete()
        return redirect('band_list')
    return render(
        request=request,
        template_name='listings/band_delete.html',
        context={'band': band}
    )

def listings(request):
    listings_instance = Listing.objects.all()
    return render(request=request,
                  template_name='listings/listings_list.html',
                  context={'listings_instance': listings_instance})

def listing_detail(request, listings_id):
    listing_instance = Listing.objects.get(id=listings_id)
    listing = listing_instance.__dict__
    band = Band.objects.get(id=listing_instance.band_id)
    return render(
        request=request,
        template_name='listings/listing_detail.html',
        context={'listing_instance': listing_instance, 'listing': listing, 'band': band}
    )

def listings_create(request):
    if request.method == 'POST':
        form = ListingsForm(request.POST)
        if form.is_valid():
            listing = form.save()
            return redirect('listing_detail', listing.id)
    else:
        form = ListingsForm()
    return render(
        request=request,
        template_name='listings/listings_create.html',
        context={'form': form}
    )

def listing_update(request, listings_id):
    listing = Listing.objects.get(id=listings_id)
    if request.method == 'POST':
        form = ListingsForm(request.POST,instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listing_detail', listing.id)
    else:
        form = ListingsForm(instance=listing)
    return render(
        request=request,
        template_name='listings/listing_update.html',
        context={'form': form}
    )

def listing_delete(request, listings_id):
    listing = Listing.objects.get(id=listings_id)
    if request.method == 'POST':
        listing.delete()
        return redirect('listings')
    return render(
        request=request,
        template_name='listings/listing_delete.html',
        context={'listing': listing}
    )

def contact(request):
    if request.method == 'POST':

        form = ContactUsForm(request.POST)
        #form.cleaned_data is a dict with form data after validation
        if form.is_valid():
            send_mail(
                subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via MerchEx Contact Us form',
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=['charlesforgerad@gmail.com']
            )
            return redirect('email_sent') 
    else:
        form = ContactUsForm()
    print('La méthode de requête est : ', request.method)
    print('Les données POST sont : ', request.POST)
    return render(
        request=request,
        template_name='listings/contact.html',
        context={'form': form}
    )

def email_sent(request):
    return render(
        request=request,
        template_name='listings/email_sent.html'
    )

def about(request):
    return HttpResponse('<h1>About</h1> <p>page des about-us</p>')


