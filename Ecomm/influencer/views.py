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