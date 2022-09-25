from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from furniturestore.models import Furniture,Order,User
from furniturestore.serializers import FurnitureSerializer,OrderSerializer,UserSerializer
from bson.objectid import ObjectId
import bson
import jwt
import bcrypt
import datetime
import random
import string
from django.core.mail import send_mail

from django. conf import settings
#POST GET PUT DELETE FOR FURNITURE
@csrf_exempt
@api_view(['GET','PUT','POST',])
def furnitureApi(request):
    #GET FURNITURES
    if request.method == 'GET':
        print('GET FURNITURES')
        furnitures = Furniture.objects.all()
        furnitures_serializer = FurnitureSerializer(furnitures,many=True)
        return JsonResponse(furnitures_serializer.data,safe=False)
    #ADD FURNITURE ITEM
    elif request.method == 'POST':
        furniture_data =JSONParser().parse(request)
        print(request)
        print(furniture_data['name'])
       
        furnitures_serializer = FurnitureSerializer(data=furniture_data)
        if furnitures_serializer.is_valid():
            furnitures_serializer.save()
            return Response(furniture_data,status=status.HTTP_201_CREATED)
        return JsonResponse("Failed to add ",safe=False)
    #UPDATE FURNITURE ITEM
    elif request.method == 'PUT':
        furniture_data = JSONParser().parse(request)
        print(furniture_data)
        print(ObjectId(furniture_data['_id']))
        furniture=Furniture.objects.get(_id=ObjectId(furniture_data['_id']))
        furnitures_serializer= FurnitureSerializer(furniture,data=furniture_data)
        if furnitures_serializer.is_valid():
            furnitures_serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Failed to update",safe=False)

@csrf_exempt
@api_view(['GET','DELETE'])
def furnitureApi_detail(request,id):
    try:
      furniture =  Furniture.objects.get(_id=ObjectId(id))
    except (Furniture.DoesNotExist,bson.errors.InvalidId,TypeError):
        return JsonResponse("Furniture does not exist",status=404,safe=False)

    #GET FURNITURE ITEM
    if request.method == 'GET':
        furniture_serializer = FurnitureSerializer(furniture)
        return JsonResponse(furniture_serializer.data,safe=False)
    #DELETE FURNITURE ITEM
    elif request.method == 'DELETE':
        furniture.delete()
        return JsonResponse("Deleted Successfully",safe=False)


@csrf_exempt
@api_view(['GET','PUT','POST','DELETE'])
def ordersApi(request):
    #GET ORDERS
    if request.method == 'GET':
        print('GET FURNITURES')
        orders = Order.objects.all()
        orders_serializer = OrderSerializer(orders,many=True)
        return JsonResponse(orders_serializer.data,safe=False)
    #ADD ORDER ITEM
    elif request.method == 'POST':
        order_data =JSONParser().parse(request)
        #loop to check if items exist since ArrayReferenceField doesn't work properly
        for idx,i in enumerate(order_data["items"]):
            try:
                furniture =  Furniture.objects.get(_id=ObjectId(i['_id']))
            except (Furniture.DoesNotExist,bson.errors.InvalidId,TypeError):
                return JsonResponse("Furniture does not exist",status=404,safe=False)
            print(order_data)

        orders_serializer = OrderSerializer(data=order_data)
        
        print(orders_serializer.is_valid())
        print(orders_serializer.errors)
        if orders_serializer.is_valid():
            orders_serializer.save()
            return Response(order_data,status=status.HTTP_201_CREATED)
        return JsonResponse("Failed to add ",safe=False)
    #UPDATE ORDER ITEM
    elif request.method == 'PUT':
        order_data = JSONParser().parse(request)
        print(order_data)
        print(ObjectId(order_data['_id']))
        order=Order.objects.get(_id=ObjectId(order_data['_id']))
        orders_serializer= OrderSerializer(order,data=order_data)
        if orders_serializer.is_valid():
            orders_serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Failed to update",safe=False)
@csrf_exempt
@api_view(['GET','DELETE'])
def ordersApi_detail(request,id):
    try:
      order =  Order.objects.get(_id=ObjectId(id))
    except (Order.DoesNotExist,bson.errors.InvalidId,TypeError):
        return JsonResponse("Order does not exist",status=404,safe=False)

    #GET FURNITURE ITEM
    if request.method == 'GET':
        order_serializer = OrderSerializer(order)
        return JsonResponse(order_serializer.data,safe=False)
    #DELETE FURNITURE ITEM
    elif request.method == 'DELETE':
        order.delete()
        return JsonResponse("Deleted Successfully",safe=False)



@csrf_exempt
@api_view(['GET','PUT','POST','DELETE'])
def usersApi(request):
    #GET USERS
    if request.method == 'GET':
        print('GET users')
        users = User.objects.all()
        users_serializer = UserSerializer(users,many=True)
        return JsonResponse(users_serializer.data,safe=False)
    #ADD USER ITEM
    elif request.method == 'POST':
        user_data =JSONParser().parse(request)
        #hash password
        try:
            encodedPassword=user_data.get('password').encode('utf-8')
            user_data['password']= bcrypt.hashpw(encodedPassword,salt=bcrypt.gensalt())
            print(user_data['password'])
            user_data['password'] = user_data['password'].decode('utf-8')
        except (ValueError, TypeError) as e:
            print(e)
            return JsonResponse('Password error',status=500,safe=False)
        #loop to check if items exist since ArrayReferenceField doesn't work properly
        for idx,i in enumerate(user_data["cart"]):
            try:
                cartItem =  Furniture.objects.get(_id=ObjectId(i['_id']))
            except (User.DoesNotExist,bson.errors.InvalidId,TypeError):
                return JsonResponse("Furniture does not exist",status=404,safe=False)
        #loop to check if items exist since ArrayReferenceField doesn't work properly
        for idx,i in enumerate(user_data["orders"]):
            try:
                orders =  Order.objects.get(_id=ObjectId(i['_id']))
            except (User.DoesNotExist,bson.errors.InvalidId,TypeError):
                return JsonResponse("Furniture does not exist",status=404,safe=False)
        # string used for confirmation 
        confirmationString = ''.join(random.choice(string.ascii_letters) for i in range(15))
        user_data['confirmationString'] = confirmationString
        users_serializer = UserSerializer(data=user_data)
        print(user_data['email'])
        if users_serializer.is_valid():
            send_mail('Confirmation Email for Tree','Hello you have signed up for our website! Called Tree.Click the link to confirm you account http://127.0.0.1:8000/confirmation/'+confirmationString,
            'testovtestov22@gmail.com',[user_data['email']],fail_silently=False) 
            users_serializer.save()
            return Response(user_data,status=status.HTTP_201_CREATED)
        return JsonResponse("Failed to add ",safe=False)
    #UPDATE User ITEM
    elif request.method == 'PUT':
        user_data = JSONParser().parse(request)
        user=User.objects.get(_id=ObjectId(user_data['_id']))
        users_serializer= UserSerializer(user,data=user_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Failed to update",safe=False)

@csrf_exempt
@api_view(['GET','DELETE'])
def usersApi_detail(request,id):
    try:
      user =  Order.objects.get(_id=ObjectId(id))
      print(user)
    except (Order.DoesNotExist,bson.errors.InvalidId,TypeError):
        return JsonResponse("User does not exist",status=404,safe=False)

    #GET User ITEM
    if request.method == 'GET':
        user_serializer = OrderSerializer(user)
        return JsonResponse(user_serializer.data,safe=False)
    #DELETE User ITEM
    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse("Deleted Successfully",safe=False)

@csrf_exempt
@api_view(['POST'])
def login(request):
    user_data =JSONParser().parse(request)
    try:
        user=User.objects.get(email=user_data['email'])
  
        passwordcheck=user.password.encode('utf-8')
        passwordNotHashed= user_data['password'].encode('utf-8')

        users_serializer= UserSerializer(user,data=user_data)
        if users_serializer.is_valid():
            if bcrypt.checkpw(passwordNotHashed,passwordcheck):
                token = jwt.encode({
                "exp": datetime.datetime.now(tz=datetime.timezone.utc),    
                'email':user_data['email'],
                "firstName":user.firstName,
                "lastName":user.lastName,
                "emailConfirmed":user.emailConfirmed,
                "username":user.username,
                "address":user.address,
                "role":user.role,
                "phone":user.phone,
                "cart":user.cart,
                "orders":user.orders},settings.JWT)
                return JsonResponse({"message":"Logged in","token":token},status=200,safe=False)
            return JsonResponse('Wrong password',status=400,safe=False)
        else :
            return JsonResponse('Wrong Email',status=400,safe=False)
    except TypeError  as e:
        print(e)
        return JsonResponse('Internal Server Error',status=505,safe=False)

@csrf_exempt
@api_view(['GET'])
def email_confirmation(request,stringConfirm):
    userToConfirm = User.objects.get(confirmationString=stringConfirm)
    print(userToConfirm.confirmationString)
    userToConfirm.emailConfirmed = True
    userToConfirm.confirmationString=""
    print(userToConfirm.confirmationString)
    if userToConfirm.confirmationString == "":
        userToConfirm.save()
        return JsonResponse("Confirmed Successfully",status=200,safe=False)
    return JsonResponse('Incorrect confirmation string',status=400,safe=False)