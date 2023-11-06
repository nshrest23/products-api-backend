from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
import rest_framework.status as api_status
from django.http import JsonResponse, HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
import products.serialzers as product_serializer
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from products.models import Product
from drf_yasg.utils import swagger_auto_schema



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
    name = request.GET.get("name")
    if name:
        message = f"Hello, {name}"
    else:
        message = "Hello World!"
    return Response({"message": message}, status=api_status.HTTP_200_OK)
    #return JsonResponse({"message": message}, status=api_status.HTTP_200_OK, content_type="application/json")


     
class UserRegister(generics.GenericAPIView):

    serializer_class = product_serializer.UserRegisterSerializer
    @swagger_auto_schema(
        tags=['user'],
        operation_summary="user registration api")  
    def post(self, request, *args, **kwargs):
        request_data = request.data
        serializer = self.serializer_class(data=request_data)
        if serializer.is_valid(raise_exception=True):
            print("Validated data", serializer.validated_data)
            user = serializer.create(serializer.validated_data)
            return JsonResponse({"userId": user.pk,"message": "User Registered Successfully!"},status=api_status.HTTP_201_CREATED)


class Login(generics.GenericAPIView):

    serializer_class = product_serializer.LoginSerializer
    @swagger_auto_schema(
        tags=['user'],
        operation_summary="user login api")  
    def post(self,request, *args, **kwargs):
        request_data = request.data
        serializer = self.serializer_class(data=request_data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=request_data["username"],
                                password=request_data["password"])
            if user:
                access_token = AccessToken.for_user(user)
                return JsonResponse({"userID": user.pk, "token": str(access_token)}, status=api_status.HTTP_200_OK)
            else: 
                return JsonResponse({"message": "Invalid User Credentials!"}, status=api_status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({"message": "User Login Failed!", "errors": serializer.errors}, status=api_status.HTTP_400_BAD_REQUEST)


class UserProfile(generics.GenericAPIView):

    serializer_class = product_serializer.UserRegisterSerializer
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        tags=['user'],
        operation_summary="user profile api")  
    def get(self, request):
        user = User.objects.get(pk=request.user.pk)
        user_data = self.serializer_class(user).data
        if "password" in user_data:
            del user_data["password"]
        return JsonResponse(user_data,status=api_status.HTTP_200_OK)
        

class ProductCreate(generics.GenericAPIView):
    serializer_class = product_serializer.ProductModelSerializer
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        tags=['products'],
        operation_summary="product create api") 
    def post(self, request):
        request_data = request.data
        serializer = self.serializer_class(data=request_data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data["user_id"] = request.user.pk
            product = serializer.create(serializer.validated_data)
            return JsonResponse({"productId": product.pk, "message": "Product Created Succefully!"}, status=api_status.HTTP_201_CREATED)
        else:
            return JsonResponse({"message": "Product creation Failed!", "errors": serializer.errrors}, status=api_status.HTTP_400_BAD_REQUEST)

        
class ProductList(generics.GenericAPIView):
    serializer_class = product_serializer.ProductModelSerializer
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        tags=['products'],
        operation_summary="product list api") 
    def get(self,request):
        products = Product.objects.all()
        product_data = self.serializer_class(products, many=True).data
        return JsonResponse(product_data, status=api_status.HTTP_200_OK, safe=False)
    
class ProductDetail(generics.GenericAPIView):
    serializer_class = product_serializer.ProductModelSerializer
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        tags=['products'],
        operation_summary="product detail api") 
    def get(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
            product_data = self.serializer_class(product).data
            return JsonResponse(product_data, status = api_status.HTTP_200_OK)
        except Product.DoesNotExist:
            return JsonResponse({"message": "Product Doesnot Exists"}, status = api_status.HTTP_404_NOT_FOUND)
        
class ProductUpdate(generics.GenericAPIView):
    serializer_class = product_serializer.ProductModelSerializer
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        tags=['products'],
        operation_summary="product update api") 
    def put(self, request, product_id):
        try:
            request_data = request.data
            serializer = self.serializer_class(data=request_data)
            if serializer.is_valid(raise_exception=True):
                product = Product.objects.get(pk=product_id)
                product = serializer.update(product, serializer.validated_data)
                return JsonResponse({"productID": product.pk, "message": "Product updates succeffuly!"}, status = api_status.HTTP_200_OK)
            else:
                return JsonResponse({"message": "Product update Failed!"}, status = api_status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return JsonResponse({"message": "Product doesnot Exists!"}, status = api_status.HTTP_404_NOT_FOUND)

class ProductDelete(generics.GenericAPIView):
    serializer_class = product_serializer.ProductModelSerializer
    permission_classes = [ IsAuthenticated ]
    @swagger_auto_schema(
        tags=['products'],
        operation_summary = "product delete api")
    def delete(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
            Product.objects.filter(pk=product_id).delete()
            return JsonResponse({"productID": product_id, "message": "Product Successfully deleted!"}, status = api_status.HTTP_200_OK, safe=False)
        except Product.DoesNotExist:
            return JsonResponse({"message": "Product does not exists"}, status = api_status.HTTP_404_NOT_FOUND)
        
