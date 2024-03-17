from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Otp,CustomUser
# Create your views here.
@login_required(login_url='backend/login')
def dashboard(request):
    return render(request,'backend/dashboard.html')
@login_required(login_url='backend/login')
def charts(request):
    return render(request,"backend/charts.html")

from django.contrib.auth import get_user_model  # Import get_user_model
from django.contrib.auth.models import User  # Import the User model

from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth.models import User
from django.utils import timezone

def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()  # Use User model
        if user and user.is_staff:
            # Generate OTP
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

            # Send OTP email
            subject = 'OTP for Password Change'
            message = f'Your OTP for password change is: {otp}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)

            # Store OTP and its creation time in database
            otp_obj, created = Otp.objects.get_or_create(user=user)
            otp_obj.otp = otp
            otp_obj.otp_created_at = timezone.now()
            otp_obj.save()

            return redirect('verify_otp')
        else:
            error = "Email does not exist or user is not authorized."
            return render(request, 'send_otp.html', {'error': error})
    return render(request, 'send_otp.html')

def verify_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email, is_staff=True).first()
        if user:
            # Generate OTP
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

            # Send OTP email
            subject = 'OTP for Email Verification'
            message = f'Your OTP for email verification is: {otp}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)

            # Store OTP and its creation time in database
            otp_obj, created = Otp.objects.get_or_create(user=user)
            otp_obj.otp = otp
            otp_obj.otp_created_at = timezone.now()
            otp_obj.save()

            # Store email in session
            request.session['verified_email'] = email

            return redirect('verify_otp')
        else:
            error = "Email does not exist or user is not authorized."
            return render(request, 'backend/verify_email.html', {'error': error})
    return render(request, 'backend/verify_email.html')
from django.contrib import messages

def verify_otp(request):
    email = request.session.get('verified_email')
    if not email:
        # If email is not found in session, redirect to the verify_email page
        messages.error(request, 'Please verify your email first.')
        return redirect('verify_email')

    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        user = User.objects.filter(email=email).first()
        if user and user.is_staff:
            otp_obj = Otp.objects.filter(user=user).first()
            if otp_obj:
                # Check if OTP matches
                if otp_obj.otp == otp_entered:
                    # Check if OTP is expired (5 minutes expiry)
                    if (timezone.now() - otp_obj.otp_created_at).total_seconds() > 300:
                        return render(request, 'backend/verify_otp.html', {'email': email, 'error': 'OTP has expired. Please request a new OTP.'})
                    else:
                        return redirect('change_password')
                else:
                    return render(request, 'backend/verify_otp.html', {'email': email, 'error': 'Invalid OTP. Please enter the correct OTP.'})
            else:
                return render(request, 'backend/verify_otp.html', {'email': email, 'error': 'OTP not found. Please request a new OTP.'})
        else:
            error = "Otp Does Not Match!!"
            return render(request, 'backend/verify_otp.html', {'error': error})
    return render(request, 'backend/verify_otp.html', {'email': email})
from django.contrib.auth import update_session_auth_hash

def change_password(request):
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

        user = User.objects.filter(email=email).first()
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

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .models import Catagory,Stock
from django.shortcuts import render

@login_required(login_url='backend/login')
def catagory(request):
    catagoryapp=Catagory.objects.all()

    context={
        'banform': catagoryapp

    }
    return render(request,'backend/catagory.html',context)
@login_required(login_url='backend/login')
def catgoryadd(request):
    if request.method == "POST":
        contact = Catagory()
        name = request.POST.get('name')
        image = request.FILES.get('image')
        contact.name = name
        contact.image = image
        contact.save()
        return redirect('catagoryapp')
    return render(request, 'backend/catgoryadd.html')
@login_required(login_url='backend/login')
def delete_item(request, myid):
    catagoryapp=Catagory.objects.get(id=myid)
    catagoryapp.delete()
    return redirect('catagoryapp')
@login_required(login_url='backend/login')
def edit_item(request, myid):
    sel_catform=Catagory.objects.get(id=myid)
    cat = Catagory.objects.all()
    context = {
        'cat': cat,
        'sel_catform':sel_catform

    }
    return render(request,'backend/catagoryedit.html',context)
@login_required(login_url='backend/login')
def update_item(request, myid):
    catagoryapp=Catagory.objects.get(id=myid)

    catagoryapp.name = request.POST.get('name')
    if 'image' in request.FILES:
        catagoryapp.image = request.FILES['image']

    catagoryapp.save()
    return redirect('catagoryapp')
@login_required(login_url='backend/login')
def view_item(request, myid):
    sel_catform = Catagory.objects.get(id=myid)
    cat = Catagory.objects.all()
    context = {
        'catform': cat,
        'sel_catform': sel_catform

    }
    return render(request, 'backend/catagoryview.html', context)
@login_required(login_url='backend/login')
def activate_catagory(request, catagory_id):
    banner = get_object_or_404(Catagory, id=catagory_id)
    banner.status = True
    banner.save()
    return redirect('catagoryapp')  # Redirect to your banner list view
@login_required(login_url='backend/login')
def deactivate_catagory(request, catagory_id):
    banner = get_object_or_404(Catagory, id=catagory_id)
    banner.status = False
    banner.save()
    return redirect('catagoryapp')  # Redirect to your banner list view
# Create your views here.
@login_required(login_url='backend/login')
def customerlist(request):
    productapp=User.objects.all()

    context={
        'banform': productapp
    }
    return render(request,'backend/customerlist.html',context)
@login_required(login_url='backend/login')
def activate_customer(request, id):
    banner = get_object_or_404(User, id=id)
    banner.status = True
    banner.save()
    return redirect('customerlist')  # Redirect to your banner list view
@login_required(login_url='backend/login')
def deactivate_customer(request, id):
    banner = get_object_or_404(User, id=id)
    banner.status = False
    banner.save()
    return redirect('customerlist')  # Redirect to your banner list view

@login_required(login_url='backend/login')
def product(request):
    productapp=Product.objects.all()

    context={
        'banform': productapp
    }
    return render(request,'backend/product.html',context)
@login_required(login_url='backend/login')
def productadd(request):
    if request.method == "POST":
        product = Product()
        stock = Stock()
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        created_date = request.POST.get('created_date')
        coupon = request.POST.get('coupon')
        openingstock=request.POST.get('openingstock')

        image = request.FILES.get('image')
        product.name = name
        product.price = price
        product.description = description
        product.created_date =created_date
        product.coupon = coupon
         # Get the selected category ID
        cat_name = request.POST.get('cat_name')

       # Get the selected category name
        category = Catagory.objects.get(name=cat_name)  # Retrieve the Category object by name
        product.cat_name = category
        product.image = image
        stock.openingstock = openingstock
        stock.item = product
        product.save()
        stock.save()

        return redirect('productapp')
    # categories = Catagory.objects.get(status=True)
    categories = Catagory.objects.all()
    return render(request, 'backend/productadd.html',{'categories': categories})
@login_required(login_url='backend/login')
def delete_product(request, myid):
    productapp=Product.objects.get(id=myid)
    productapp.delete()
    return redirect('productapp')
@login_required(login_url='backend/login')
def edit_product(request, myid):
    sel_proform=Product.objects.get(id=myid)
    pro = Product.objects.all()
    # categories = Catagory.objects.filter(status=True)
    categories = Catagory.objects.all()
    context = {

        'pro': pro,
        'sel_proform':sel_proform,
        'categories':categories

    }
    return render(request,'backend/productedit.html',context)
@login_required(login_url='backend/login')
def update_product(request, myid):
    productapp=Product.objects.get(id=myid)

    productapp.name = request.POST.get('name')
    productapp.price = request.POST.get('price')
    productapp.description = request.POST.get('description')
    productapp.created_date = request.POST.get('created_date')
    if 'image' in request.FILES:
        productapp.image = request.FILES['image']
    cat_name = request.POST.get('cat_name')  # Get the selected category name
    category = Catagory.objects.get(name=cat_name)  # Retrieve the Category object by name
    productapp.cat_name = category

    productapp.save()

    return redirect('productapp')
@login_required(login_url='backend/login')
def view_product(request, myid):
    sel_proform = Product.objects.get(id=myid)
    pro = Product.objects.all()
    context = {
        'proform': pro,
        'sel_proform': sel_proform

    }
    return render(request, 'backend/productview.html', context)
@login_required(login_url='backend/login')
def activate_product(request, product_id):
    banner = get_object_or_404(Product, id=product_id)
    banner.status = True
    banner.save()
    return redirect('productapp')  # Redirect to your banner list view
@login_required(login_url='backend/login')
def deactivate_product(request, product_id):
    banner = get_object_or_404(Product, id=product_id)
    banner.status = False
    banner.save()
    return redirect('productapp')  # Redirect to your banner list view
# Create your views here.
from .models import CustomerCoupon
@login_required(login_url='backend/login')
def add_customer_coupon(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customerName')
        occasion_name = request.POST.get('occasionName')
        expire_date = request.POST.get('expireDate')
        coupon_value = request.POST.get('couponValue')
        coupon_type = request.POST.get('couponType')
        description = request.POST.get('description')
        # Assuming 'occasion_name' is the name of the occasion for which the coupon is issued

        customer_coupon = CustomerCoupon(
            customer=customer_name,
            occasion=occasion_name,
            expire_date=expire_date,
            coupon_value=coupon_value,
            coupon_type=coupon_type,
            description=description
        )
        customer_coupon.save()

        return redirect('customer_couponlist')  # Redirect to the desired page after submission

    return render(request, 'backend/add_customer_coupon.html')
@login_required(login_url='backend/login')
def customer_couponlist(request):
    coupons = CustomerCoupon.objects.all()
    return render(request, 'backend/customercouponlist.html', {'coupons': coupons})
from django.shortcuts import get_object_or_404
@login_required(login_url='backend/login')
def delete_coupon(request, coupon_id):
    coupon = get_object_or_404(CustomerCoupon, pk=coupon_id)
    coupon.delete_coupon()
    # Optionally, add a success message or redirect to a different page
    return redirect('customer_couponlist')
@login_required(login_url='backend/login')
def activate_coupon(request, coupon_id):
    banner = get_object_or_404(CustomerCoupon, id=coupon_id)
    banner.status = True
    banner.save()
    return redirect('customer_couponlist')  # Redirect to your banner list view
@login_required(login_url='backend/login')
def deactivate_coupon(request, coupon_id):
    banner = get_object_or_404(CustomerCoupon, id=coupon_id)
    banner.status = False
    banner.save()
    return redirect('customer_couponlist')  # Redirect to your banner list view