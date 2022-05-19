from django.urls import path
from .views import *

urlpatterns = [
    path('', Main.as_view(), name='home'),
    path('currency/', Currency.as_view(), name='currency'),
    path('converter/', Converter.as_view(), name='converter'),
]
