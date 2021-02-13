from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import path,include
from main import views


urlpatterns = [
    path('payments/', views.PaymentListView.as_view()),
    path('payments/<start_date>/<end_date>', views.Payment_range_view.as_view()),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
