from django.urls import path
from main import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('payments/', views.payment_list_view),
    path('payments/<int:pk>/', views.payment_view),
]

urlpatterns = format_suffix_patterns(urlpatterns)