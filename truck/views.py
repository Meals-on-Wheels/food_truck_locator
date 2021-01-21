from django.shortcuts import render, redirect, reverse
from .models import TruckInstance, ImageLink, MenuItem, OrderInstance
from django.http import HttpResponse, HttpRequest
from django.views import View, generic
from django import forms
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode, urlencode
from . import tokens
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from .forms import TruckDetailForm
import json

class SignUpForm(UserCreationForm):
    firstName = forms.CharField(max_length=40, required=True)
    lastName = forms.CharField(max_length=40, required=False)
    email = forms.EmailField(max_length=100)
    phone = forms.CharField(max_length=18)

    class Meta:
        model = User
        fields = ('username', 'firstName', 'lastName', 'email', 'phone', 'password1', 'password2')

def SignUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False 
            user.save()
            currentSite = get_current_site(request)
            subject = 'Activate Account'
            base_url = reverse('activate')
            query = urlencode({'uidb64': user.pk, 'token': tokens.activate_account_token.make_token(user)})
            url = '{}?{}'.format(base_url, query)
            message = render_to_string('activate_account_email.html', {
                'user': user,
                'domain': currentSite.domain,
                'url': url,
            })

            cleaned_email = form.cleaned_data.get('email')
            email = EmailMessage(subject, message, to=[cleaned_email])
            email.send()
            return redirect('activate_account_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def signIn(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
    


# , uidb64, token

def activate(request):
    user, token = None, None
    try:
        token = request.GET.get('token')
        uid = request.GET.get('uidb64')
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist): # User.ObjectDoesNotExist?
        user = None if not user else user
        token = None if not token else token

    if user is not None and tokens.activate_account_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        #return redirect('home')
        return('index')
    else:
        return render(request, "Link is invalid")

def activate_account_sent(request):
    return render(request, "activate_account_sent.html")

def activate_account_invalid(request):
    return render(request, "activate_account_invalid.html")

# request.query.lat ???
def test_map_view(request):
    info = {
        'lat': 40.714224,
        'lng': -73.961452
    }
    return render(
        request, "map2.html", context = info
    )

def home_view(request, *args, **kwargs):
    return render(request, "index.html", {})

def login_view(request, *args, **kwargs):
    return render(request, "login.html", {})

def signup_view(request, *args, **kwargs):
    return render(request, "signup.html", {})


# home view for after logging in?



# def order_detail_view(request, *args, **kwargs):
    # truck = TruckInstance.get(id=request.truck)
    # context={'orders': truck.list_menu(),}
    # return render(request, "order-detail.html", context)

def about_view(request, *args, **kwargs):
    return render(request, "about.html", {})

def _redirect(request, *args, **kwargs):
    return redirect(request, 'index.html', {})

#### Completed order for passing information
def truck_list_view(request, *args, **kwargs):
    #when we link to this we need a propery to say if its from the owner like below
    # if request.owned:
    #     context = {'trucks': TruckInstance.objects.all().filter(owner=request.user)}
    # else:
    context = {'trucks': TruckInstance.objects.all()}
    return render(request, "truck-list-view.html", context)
    # should have view of the map inside

def truck_single_view(request, *args, **kwargs):
    # truck = TruckInstance.objects.get(id=request.POST['truck'])
    truck = TruckInstance.objects.get(pk=request.POST['truck'])
    context={'truck': truck,}
    return render(request, "truck-single-view.html", context)

## Need to think of a way to grab all the food quantities selected and create the orderinstance
def menu_page_view(request, *args, **kwargs):
    if 'inventory' in request.POST:
        new_order = OrderInstance.objects.create(poster=request.user, truck=TruckInstance.objects.get(pk=request.POST['truck']))
        inventory = request.POST['inventory']
        for item in inventory.split(', '):
            new_order.inventory.add(MenuItem.objects.get(pk=int(item)))
        new_order.save()
        base_url = reverse('checkout')
        query = urlencode({'order': new_order.pk})
        url = '{}?{}'.format(base_url, query)
        return redirect(url)
    truck = TruckInstance.objects.get(pk=request.POST['truck'])
    context={'truck': truck}
    return render(request, "menu-page.html", context)

def checkout_view(request, *args, **kwargs):
    order_number = request.GET.get('order')
    context={'orders': OrderInstance.objects.get(pk=order_number).list_inventory(),}
    return render(request, "checkout.html", context)

def all_orders_view(request, *args, **kwargs):
    if 'poster' in request.POST:
        OrderInstance.objects.get(poster=User.objects.get(username=request.POST['poster']), truck=TruckInstance.objects.get(pk=request.POST['truck'])).delete()
    truck = TruckInstance.objects.get(pk=request.POST['truck'])
    context={'orders': OrderInstance.objects.filter(truck=truck),}
    return render(request, "all-orders.html", context)