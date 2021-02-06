from django.urls import path,include
from main import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('payments/', views.Payment_list_view.as_view()),
    #path('payments/<int:pk>/', views.Payment_view.as_view()),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)