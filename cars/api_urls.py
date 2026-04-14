from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cars import api_views




router = DefaultRouter()
router.register('', api_views.CarViewSet, basename='car')



urlpatterns = [
    path('my-cars/', api_views.UserCarListAPIView.as_view(), name='my-cars'),
    path('', include(router.urls)),
]