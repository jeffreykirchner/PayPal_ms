from django.urls import path
from main import views

urlpatterns = [
    path('payments/', views.payment_list_view),
    path('payments/<int:pk>/', views.payment_view),
]