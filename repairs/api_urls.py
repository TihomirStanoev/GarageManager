from django.urls import path, include
from rest_framework.routers import DefaultRouter
from repairs import api_views



router = DefaultRouter()
router.register('parts', api_views.PartViewSet, basename='part')
router.register('manager', api_views.RepairManagerViewSet, basename='manager')
router.register('mechanic', api_views.RepairMechanicViewSet, basename='mechanic')




urlpatterns = [
    path('', include(router.urls)),
    path('my-repairs/', api_views.RepairListAPIView.as_view(), name='my_repairs'),

]