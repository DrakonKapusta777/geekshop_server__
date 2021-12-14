from django.urls import path
import basketapp.views as basket


app_name = 'basketapp'

urlpatterns = [
    path('', basket.basket, name='basket'),
    path('add/<int:pk>/', basket.add, name='add'),
    path('remove/<int:pk>)/', basket.remove, name='remove'),
]
