from django.urls import path
import products.views as productapi


urlpatterns = [
    path('', productapi.home),
    path('register/', productapi.UserRegister.as_view(), name="user_registration"),
    path('login/', productapi.Login.as_view(), name="user_login"),
    path('profile/', productapi.UserProfile.as_view(), name="user_profile"),
    path('product/create', productapi.ProductCreate.as_view(), name="product_create"),
    path('product/list', productapi.ProductList.as_view(), name="product_list"),
    path('product/detail/<int:product_id>', productapi.ProductDetail.as_view(), name="product_detail"),
    path('product/update/<int:product_id>', productapi.ProductUpdate.as_view(), name="product_update"),
    path('product/delete/<int:product_id>', productapi.ProductDelete.as_view(), name="product_delete")
]