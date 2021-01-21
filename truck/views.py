from django.shortcuts import render, redirect, reverse
from .models import TruckInstance, ImageLink, MenuItem, OrderInstance
from .tokens import activate_account_token
from django.http import HttpResponse, HttpRequest
from django.utils.http import urlencode
from django.views import View, generic
from django.contrib.auth import login, authenticate, logout, tokens
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, forms
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode, urlencode
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.core.exceptions import ObjectDoesNotExist
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
            message = render_to_string('activate_account_email.html', {
                'user': user,
                'domain': currentSite.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),#.decode(),
                'token': activate_account_token.make_token(user),
            })

            cleaned_email = form.cleaned_data.get('email')
            email = EmailMessage(subject, message, to=[cleaned_email])
            email.send()
            return redirect('activate_account_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def profile_view(request, user):
    if 'remove' in request.POST:
        TruckInstance.objects.get(pk=request.POST['truck']).delete()
    if 'name' in request.POST:
        contact = '' if not 'contact' in request.POST else request.POST['contact']
        TruckInstance.objects.create(owner=request.user, name=request.POST['name'], contact=contact)
    account = User.objects.get(username=user)
    return render(request, 'truck-list-view.html', {'trucks': TruckInstance.objects.filter(owner=account), 'profile': True})
    
def logout_view(request):
    logout(request)
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist): # User.ObjectDoesNotExist?
        user = None

    if user is not None and activate_account_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
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
    if 'edit' in request.POST:
        context['edit'] = True
        if 'name' in request.POST:
            truck.name = request.POST['name']
        if 'location' in request.POST:
            truck.location = request.POST['location']
        if 'link' in request.POST:
            new_image = ImageLink.objects.create(title='' if not 'title' in request.POST else request.POST['title'], link=request.POST['link'])
            truck.album.add(new_image)
        if 'contact' in request.POST:
            truck.contact = request.POST['contact']
        truck.save()
    return render(request, "truck-single-view.html", context)

## Need to think of a way to grab all the food quantities selected and create the orderinstance
def menu_page_view(request, *args, **kwargs):
    truck = TruckInstance.objects.get(pk=request.POST['truck'])
    context={'truck': truck, 'menu': truck.menu.all()}
    if 'edit' in request.POST:
        context['edit'] = True
        if 'delete' in request.POST:
            # remove = MenuItem.objects.get(pk=request.POST['item'])
            # truck.album.remove(remove)
            MenuItem.objects.get(pk=request.POST['item']).delete()
        elif 'item' in request.POST:
            editing = MenuItem.objects.get(pk=request.POST['item'])
            editing.item = request.POST['name']
            editing.description = request.POST['description']
            editing.cost = request.POST['cost']
            editing.save()
        elif 'newitem' in request.POST:
            new = MenuItem.objects.create(item='' if not 'name' in request.POST else request.POST['name'], description='' if not 'description' in request.POST else request.POST['description'], cost=0 if not 'cost' in request.POST else request.POST['cost'])
            truck.menu.add(new)
        return render(request, "menu-page.html", context)
    else:
        context['menu_items'] = ', '.join([str(item.id) for item in truck.menu.all()])
        return render(request, "order-menu.html", context)

def checkout_view(request, *args, **kwargs):
    new_order = OrderInstance.objects.create(poster=request.user, truck=TruckInstance.objects.get(pk=request.POST['truck']))
    inventory = request.POST['inventory']
    for item in inventory.split(', '):
        grub = MenuItem.objects.get(id=int(item))
        if grub.item in request.POST:
            new_order.inventory.add(grub)
    new_order.save()
    print('***********\n***********\n***********\n', new_order.inventory.all(), '***********\n***********\n***********\n')
    context={'order': new_order.inventory.all(),}
    return render(request, "checkout.html", context)

def all_orders_view(request, *args, **kwargs):
    if 'poster' in request.POST:
        OrderInstance.objects.get(poster=User.objects.get(username=request.POST['poster']), truck=TruckInstance.objects.get(pk=request.POST['truck'])).delete()
    truck = TruckInstance.objects.get(pk=request.POST['truck'])
    context={'orders': OrderInstance.objects.filter(truck=truck),}
    return render(request, "all-orders.html", context)