from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart
from .serializers import CartSerializer,CartGetSerializer
from ecomApp.models import CustomUser
from menu_management.models import Item
from rest_framework.permissions import IsAuthenticated

class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            product_id = request.data.get('product_id')
            u_id = request.data.get('u_id')

            # Check if product with given ID exists
            product = Item.objects.filter(id=product_id).first()
            if not product:
                return Response({"error": "Product does not exist."}, status=status.HTTP_404_NOT_FOUND)

            # Check if user with given ID exists
            user = CustomUser.objects.filter(id=u_id).first()
            if not user:
                return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

            # Get the cart item for the given product and user
            cart_item, created = Cart.objects.get_or_create(product_id=product, u_id=user)

            if not created:
                # If the item already exists, increment its quantity and update its price
                cart_item.quantity += 1
                cart_item.price = cart_item.quantity * product.item_new_price  # Update the price based on the current product price
            else:
                # If the item is newly created, set its initial quantity and price
                cart_item.quantity = 1
                cart_item.price = product.item_new_price

            cart_item.save()

            # Serialize the cart item
            serializer = CartSerializer(cart_item)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CartDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get the user_id from query parameters
            user_id = request.query_params.get('user_id')

            # Validate user_id parameter
            if not user_id:
                return Response({"error": "user_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve all cart items for the specified user_id
            cart_items = Cart.objects.filter(u_id=user_id)

            # Serialize the cart items
            serializer = CartGetSerializer(cart_items, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class IncreaseQuantity(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cart_id = request.data.get('cart_id')

            # Retrieve the cart item
            cart_item = Cart.objects.get(id=cart_id)

            # Increment quantity
            cart_item.quantity += 1
            cart_item.save()

            # Update total price
            cart_item.price = cart_item.product_id.item_new_price * cart_item.quantity
            cart_item.save()

            return Response({"message": "Quantity increased successfully."}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"error": "Cart item does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DecreaseQuantity(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cart_id = request.data.get('cart_id')

            # Retrieve the cart item
            cart_item = Cart.objects.get(id=cart_id)

            # Ensure quantity is greater than 1 before decrementing
            if cart_item.quantity > 1:
                # Decrement quantity
                cart_item.quantity -= 1
                cart_item.save()

                # Update total price
                cart_item.price = cart_item.product_id.item_new_price * cart_item.quantity
                cart_item.save()

                return Response({"message": "Quantity decreased successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Quantity cannot be less than 1."}, status=status.HTTP_400_BAD_REQUEST)
        except Cart.DoesNotExist:
            return Response({"error": "Cart item does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RemoveCartItem(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            cart_id = request.query_params.get('cart_id')

            # Check if cart_id parameter is provided and if it's a valid integer
            if not cart_id.isdigit():
                return Response({"error": "Valid cart_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve the cart item
            cart_item = Cart.objects.get(id=int(cart_id))

            # Delete the cart item
            cart_item.delete()

            return Response({"message": "Cart item removed successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({"error": "Cart item does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "Invalid cart_id provided."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CartTotalPrice(APIView):
    def get(self, request):
        try:
            # Get the user_id from query parameters
            user_id = request.query_params.get('user_id')

            # Check if user_id parameter is provided
            if user_id is None:
                return Response({"error": "user_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Check if user_id is a valid integer
            if not str(user_id).isdigit():
                return Response({"error": "Valid user_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve all cart items for the specified user_id
            cart_items = Cart.objects.filter(u_id=user_id)

            # Calculate total price by summing the prices of all cart items
            total_price = sum(cart_item.price for cart_item in cart_items)

            return Response({"total_price": total_price}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
