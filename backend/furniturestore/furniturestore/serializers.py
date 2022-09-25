from rest_framework import serializers
from furniturestore.models import Furniture
from furniturestore.models import Order,User
class FurnitureSerializer(serializers.ModelSerializer):
    class Meta:
        model=Furniture
        fields=('_id','name','hasWarranty','isPopular','price','quantity','stock','description','categoryArray','materialArray','ratings',)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=('_id','items','totalValue','sent','delivered','ordered','message','userId','orderPaid','paypalOrderId')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('_id','firstName','lastName','email','username','password','cart','orders','emailConfirmed','role','phone','confirmationString')
