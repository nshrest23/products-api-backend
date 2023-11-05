from django.urls import path
import products.views as productapi


urlpatterns = [
    path('', productapi.home),
    path('register/', productapi.UserRegister.as_view(), name="user_registration"),
    path('login/', productapi.Login.as_view(), name="user_login"),
    path('profile/', productapi.UserProfile.as_view(), name="user_profile"),
    path('product/create', productapi.ProductCreate.as_view(), name="product_create"),
    path('product/list', productapi.ProductList.as_view(), name="product_list")
]