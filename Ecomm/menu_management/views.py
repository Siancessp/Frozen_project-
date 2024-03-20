from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Item
from ecomApp.models  import Catagory
from django.db.models import Q# Create your views here.
@login_required(login_url='backend/login')
def item_list(request):
    items = Item.objects.all()

    context = {
        'items': items
    }
    return render(request, 'backend/item_list.html', context)

@login_required(login_url='backend/login')
def add_item(request):
    if request.method == "POST":
        title=request.POST.get('title')
        weight_units=request.POST.get('weight_units')
        description=request.POST.get('description')
        item_photo = request.FILES.get('item_photo')
        item_quantity = request.POST.get('item_quantity')
        item_old_price = request.POST.get('item_old_price')
        discount = request.POST.get('discount')
        category_id = request.POST.get('category')
        deal_of_the_day = request.POST.get('deal_of_the_day') == 'on'
        recommended = request.POST.get('recommended') == 'on'
        most_popular = request.POST.get('most_popular') == 'on'

        # Calculate item_new_price based on item_old_price and discount
        item_new_price = float(item_old_price) * (1 - float(discount) / 100)


        # Create the item object
        item = Item.objects.create(
            title=title,
            item_measurement=weight_units,
            description=description,
            item_photo=item_photo,
            item_quantity=item_quantity,
            item_old_price=item_old_price,
            discount=discount,
            item_new_price=item_new_price,
            status=True,
            category_id=category_id,
            most_popular=most_popular,
            recommended=recommended,
            deal_of_the_day=deal_of_the_day
        )
        return redirect('item_list')

    # If the request method is not POST, render the form
    categories = Catagory.objects.all()
    return render(request, 'backend/add_item.html', {'categories': categories})

@login_required(login_url='backend/login')
def activate_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.status = True
    item.save()
    return redirect('item_list')

@login_required(login_url='backend/login')
def deactivate_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.status = False
    item.save()
    return redirect('item_list')

@login_required(login_url='backend/login')
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect('item_list')

@login_required(login_url='backend/login')
def view_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'backend/view_item.html', {'item': item})

@login_required(login_url='backend/login')
def deal_of_the_day(request):
    items = Item.objects.all()
    items = [item for item in items if item.deal_of_the_day]
    context = {
        'items': items
    }
    return render(request, 'backend/deal_of_the_day.html', context)
@login_required(login_url='backend/login')
def recommended(request):
    items = Item.objects.all()
    items = [item for item in items if item.recommended]
    context = {
        'items': items
    }
    return render(request, 'backend/recommended.html', context)

@login_required(login_url='backend/login')
def most_popular(request):
    items = Item.objects.all()
    items = [item for item in items if item.most_popular]
    context = {
        'items': items
    }
    return render(request, 'backend/most_popular.html', context)

@login_required(login_url='backend/login')
def update_item(request, item_id):
    edit_item = get_object_or_404(Item, id=item_id)

    try:
        item_photo = request.FILES.get('item_photo')
        if item_photo:
            edit_item.item_photo = item_photo
        edit_item.title = request.POST.get('title')
        edit_item.item_measurement = request.POST.get('item_measurement')

        edit_item.description = request.POST.get('description')
        edit_item.item_quantity = request.POST.get('item_quantity')
        edit_item.item_old_price = request.POST.get('item_old_price')
        edit_item.discount = request.POST.get('discount')
        edit_item.item_new_price = request.POST.get('item_new_price')
        edit_item.category_id = request.POST.get('category')  # Assuming you're passing category id from the form
        edit_item.save()
        return redirect('item_list')  # Redirect to item list page after successful update
    except Exception as e:
            # If an error occurs during update, handle it here
        error_message = f'Error occurred while updating item: {e}'
        return render(request, 'backend/edit_item.html', {'item': edit_item, 'message': error_message})

    return render(request, 'backend/edit_item.html', {'item': edit_item})

@login_required(login_url='backend/login')
def edit_item(request, item_id):
    sel_item = get_object_or_404(Item, id=item_id)
    all_items = Item.objects.all()
    categories = Catagory.objects.all()

    context = {
        'all_items': all_items,
        'item': sel_item,
        'categories':categories
    }
    return render(request, 'backend/edit_item.html', context)

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Item
from .serializers import ItemSerializer,CategorySerializer

class DealOfTheDayAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = Item.objects.all()
        items = [item for item in items if item.deal_of_the_day and item.status]
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

class RecommendedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = Item.objects.all()
        items = [item for item in items if item.recommended and item.status]
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

class MostPopularAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = Item.objects.all()
        items = [item for item in items if item.most_popular and item.status]
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

class AllProduct(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = Item.objects.all()
        items = [item for item in items if item.status]
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
from django.http import Http404
from rest_framework import status
class CategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the category ID from the query parameters
        category_id = request.query_params.get('category_id')

        try:
            # Fetch items for the specified category ID
            items = Item.objects.filter(category__id=category_id)
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data)
        except Item.DoesNotExist:
            return Response({"error": "Category does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategoryFetch(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Fetch all categories
            categories = Catagory.objects.filter( status=True)

            # Serialize the categories
            category_serializer = CategorySerializer(categories, many=True)

            return Response(category_serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategoryfiveFetch(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Fetch all categories
            categories = Catagory.objects.filter(status=True)[:5]

            # Serialize the categories
            category_serializer = CategorySerializer(categories, many=True)

            return Response(category_serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DealOfTheDayfiveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = Item.objects.filter(deal_of_the_day=True, status=True)[:5]  # Fetch only the first five items
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

class RecommendedfiveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = Item.objects.filter(recommended=True , status=True)[:5]  # Fetch only the first five items
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

class MostPopularfiveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = Item.objects.filter(most_popular=True , status=True)[:5]  # Fetch only the first five items
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

class AllfiveProduct(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = Item.objects.filter(status=True)[:5]  # Fetch only the first five items
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
