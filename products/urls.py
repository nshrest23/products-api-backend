from django.urls import path
import products.views as productapi


urlpatterns = [
    path('', productapi.home),
]