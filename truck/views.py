from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django import forms
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from . import tokens
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist

class SignUpForm(UserCreationForm):
    firstName = forms.CharField(max_length=40, required=True)
    lastName = forms.CharField(max_length=40, required=False)
    email = forms.EmailField(max_length=100)
    phone = forms.IntegerField(max_length=15)

    class Meta:
        model = User
        fields = ('username,' 'firstName', 'lastName', 'email', 'phone', 'password1', 'password2')

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
                'uid': urlsafe_base64_decode(force_bytes(user.pk)).decode(),
                'token': tokens.activate_account_token.make_token(user),
            })
            configureEmail = settings.DEFAULT_FROM_EMAIL
            send_mail(subject, message, configureEmail, [user.email])

            return HttpResponse('Please confirm your email address to complete your sign up!')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.ObjectDoesNotExist): # User.ObjectDoesNotExist?
        user = None

    if user is not None and tokens.activate_account_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('Homepage')
    else:
        return render(request, "activate_account_invalid.html")

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

