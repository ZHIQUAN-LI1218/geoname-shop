from django.urls import path, include
from .views import FeatureListView, FeatureDetailView

app_name = 'features'

urlpatterns = [
    path('', FeatureListView.as_view(), name='list'),
    path('<int:pk>/', FeatureDetailView.as_view(), name='detail'),
]
