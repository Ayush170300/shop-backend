from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializer import UserSerializer, RegisterSerializer
import json
from login.models import Order,Product
from django.contrib.auth.models import User
# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user




class ProductAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)


    def get(self,request,*args, **kwargs):
        productlist=list(Product.objects.values())
        return Response({"products":productlist})

    
    def post(self,request):
        body=json.loads(request.body.decode("utf-8"))
        
        try:
            product=Product()
            product.product_id=body['product_id']
            product.title=body['title']
            product.description=body['description']
            product.price=body['price']
            product.image_url=body['image_url']
            product.save()

            return Response({'success':True,'object':body})
        
        except  Exception as e:
            print(e)
            return Response({'success':False,'error':True})


class OrderAPI(generics.GenericAPIView):
    permission_classes=(permissions.IsAuthenticated,)


    def get(self,request):
        user_id=request.user.id
        
        user=User.objects.get(id=user_id)
        resp=[]
        orderset=Order.objects.filter(user=user)
        for order in orderset:
            resp.append({
                "user_id":order.user.id,
                "product_id":order.product.product_id,
                "title":order.product.title,
                "img_url":order.product.image_url,
                "price":order.product.price,
                "date":order.created_on
            })


        return Response({"orderlist":resp})

    
    def post(self,request):
        body=json.loads(request.body.decode("utf-8"))
        user_id=body.get("user_id",None)
        product_id=body.get("product_id",None)
        qty=body.get("qty",None)
        
        try:
            if user_id is not None and product_id is not None:
                user=User.objects.get(id=user_id)
                product=Product.objects.get(product_id=product_id)
            else:
                raise ValueError("user_id or product_id not present")

            order=Order()
            order.product=product
            order.user=user
            if qty:
                order.qty=qty
            order.save()
            return Response({"sucess":True,"user_id":order.user.id,"product_id":order.product.product_id,"created_on":order.created_on})

        except Exception as e:
            print(e)
            return Response({"error":True})




        

