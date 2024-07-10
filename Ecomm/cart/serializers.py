from rest_framework import serializers
from .models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product_id'] = instance.product_id.id
        representation['item_photo'] = instance.product_id.item_photo.url if instance.product_id.item_photo else None
        representation['product_image'] = instance.product_id.item_photo.url if instance.product_id.item_photo else None
        representation['item_new_price'] = "{:.2f}".format(instance.product_id.item_new_price)
        representation['totalPrice'] = "{:.2f}".format(instance.price)
        representation['title'] = instance.product_id.title
        representation['product_name'] = instance.product_id.title
        return representation

class CartGetSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product_id.title', read_only=True)
    product_image = serializers.URLField(source='product_id.item_photo', read_only=True)
    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        return "{:.2f}".format(obj.price)
    class Meta:
        model = Cart
        fields = ['id', 'product_id', 'u_id', 'quantity', 'price', 'product_name', 'product_image']