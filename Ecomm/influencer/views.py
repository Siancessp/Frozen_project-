from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Influencer
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Influencer
from django.contrib.auth.hashers import make_password


@login_required(login_url='backend/login')
def influencer_list(request):
    influencers = Influencer.objects.all().order_by('-id')
    return render(request, 'backend/influencer_list.html', {'influencers': influencers})


@login_required(login_url='backend/login')
def add_influencer(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        passbook = request.POST.get('pass')
        address = request.POST.get('address')
        type = request.POST.get('type')
        commission = request.POST.get('commission')
        code = request.POST.get('code')

        Influencer.objects.create(
            name=name,
            email=email,
            phone=phone,
            password=password,
            address=address,
            type=type,
            commission=commission,
            code=code,
            passbook=passbook
        )
        return redirect('influencer_list')

    return render(request, 'backend/add_influencer.html')


@login_required(login_url='backend/login')
def edit_influencer(request, influencer_id):
    influencer = get_object_or_404(Influencer, id=influencer_id)
    if request.method == "POST":
        influencer.name = request.POST.get('name')
        influencer.email = request.POST.get('email')
        influencer.phone = request.POST.get('phone')
        influencer.password = request.POST.get('password')
        influencer.address = request.POST.get('address')
        influencer.passbook = request.POST.get('pass')
        influencer.type = request.POST.get('type')
        influencer.commission = request.POST.get('commission')
        influencer.code = request.POST.get('code')

        influencer.save()
        return redirect('influencer_list')

    return render(request, 'backend/edit_influencer.html', {'influencer': influencer})


@login_required(login_url='backend/login')
def delete_influencer(request, influencer_id):
    influencer = get_object_or_404(Influencer, id=influencer_id)
    influencer.delete()
    return redirect('influencer_list')


@login_required(login_url='backend/login')
def view_influencer(request, influencer_id):
    influencer = get_object_or_404(Influencer, id=influencer_id)
    return render(request, 'backend/view_influencer.html', {'influencer': influencer})
@login_required(login_url='backend/login')
def update_influencer(request, influencer_id):
    influencer = get_object_or_404(Influencer, id=influencer_id)

    if request.method == "POST":
        influencer.name = request.POST.get('name')
        influencer.email = request.POST.get('email')
        influencer.phone = request.POST.get('phone')

        influencer.password=  request.POST.get('password')
        influencer.address = request.POST.get('address')
        influencer.passbook = request.POST.get('pass')
        influencer.type = request.POST.get('type')
        influencer.commission = request.POST.get('commission')
        influencer.code = request.POST.get('code')

        influencer.save()
        return redirect('influencer_list')

    return render(request, 'backend/edit_influencer.html', {'influencer': influencer})

@login_required(login_url='backend/login')
def view_influencer(request, influencer_id):
    influencer = get_object_or_404(Influencer, id=influencer_id)
    return render(request, 'backend/view_influencer.html', {'influencer': influencer})

@login_required(login_url='backend/login')
def activate_influencer(request, influencer_id):
    influencer = get_object_or_404(Influencer, id=influencer_id)
    influencer.status = True
    influencer.save()
    return redirect('influencer_list')

@login_required(login_url='backend/login')
def deactivate_influencer(request, influencer_id):
    influencer = get_object_or_404(Influencer, id=influencer_id)
    influencer.status = False
    influencer.save()
    return redirect('influencer_list')


from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import Influencer

class InfluencerBackend(BaseBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        try:
            influencer = Influencer.objects.get(phone=phone)
            if password == influencer.password:
                return influencer
        except Influencer.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Influencer.objects.get(pk=user_id)
        except Influencer.DoesNotExist:
            return None
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def influencer_login(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']
        user = authenticate(request, phone=phone, password=password)
        if user is not None:
            login(request, user)
            return redirect('influencer_dashboard')  # Replace 'dashboard' with your desired redirect URL
        else:
            messages.error(request, 'Invalid phone number or password')
    return render(request, 'backend/influencer_login.html',{'error': 'Invalid login credentials'})


@login_required(login_url='influencer/login')
def influencer_dashboard(request):

    return render(request, 'backend/influencer_dashboard.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def influlogout_view(request):
    if request.user.is_authenticated:
        request.session['logged_out'] = True  # Set session variable to indicate logout
        logout(request)
    return redirect('influencer/login')



def change_influencer_password(request):
    if request.method == 'POST':
        email = request.session.get('verified_email')
        if not email:
            # If email is not found in session, redirect to the verify_email page
            messages.error(request, 'Please verify your email first.')
            return redirect('change_password')

        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'backend/change_password.html')

        user = Influencer.objects.filter(email=email).first()
        if user:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            messages.success(request, "Password changed successfully.")
            return redirect('backend/login')
        else:
            messages.error(request, "User not found.")
            return redirect('verify_email')
    return render(request, 'backend/change_password.html')