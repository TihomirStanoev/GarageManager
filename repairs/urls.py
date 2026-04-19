from django.urls import path, include
from repairs import views

app_name = 'repairs'

parts_patterns = [
    path('', views.PartListView.as_view(), name='parts_list'),
    path('create/', views.CreatePartView.as_view(), name='parts_create'),
    path('<int:pk>/', views.PartDetailView.as_view(), name='parts_detail'),
    path('<int:pk>/update/', views.UpdatePartView.as_view(), name='parts_update'),
    path('<int:pk>/delete/', views.DeletePartView.as_view(), name='parts_delete'),
    path('<int:pk>/hard-delete/', views.HardDeletePartView.as_view(), name='parts_hard_delete'),
    path('<int:pk>/restore/', views.PartRestoreView.as_view(), name='parts_restore'),
]


repairs_patterns = [
    path('', views.RepairListView.as_view(), name='repairs_list'),
    path('create/', views.RepairCreateView.as_view(), name='repairs_create'),
    path('create/<str:car_plate>/', views.create_repair_with_car, name='repairs_create_with_car'),
    path('<int:pk>/', views.RepairDetailView.as_view(), name='repairs_detail'),
    path('<int:pk>/update/', views.RepairUpdateView.as_view(), name='repairs_update'),
    path('<int:pk>/delete/', views.RepairDeleteView.as_view(), name='repairs_delete'),
    path('<int:pk>/hard-delete/', views.HardDeleteRepairView.as_view(), name='repairs_hard_delete'),
    path('<int:pk>/restore/', views.RepairRestoreView.as_view(), name='repairs_restore'),
    path('<int:repair_pk>/add_part/', views.add_part_to_repair, name='repairs_add_part'),
    path('<int:repair_pk>/assign/', views.assign_unassign_repair_to_mechanic, name='assign_unassign_repair'),
    path('<int:repair_pk>/delete_part/<int:part_pk>/', views.delete_part_from_repair, name='repairs_delete_part'),
]

urlpatterns = [
    path('', include(repairs_patterns)),
    path('parts/', include(parts_patterns)),

]
