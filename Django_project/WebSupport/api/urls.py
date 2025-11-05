from django.urls import path, include
from rest_framework.routers import DefaultRouter
from WebSupport.api import views

router = DefaultRouter()
router.register(r'receive', views.ReceiveViewSet)
router.register(r'receive_items', views.ReceiveItemsViewSet)
router.register(r'shipment', views.ShipmentViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('CompanySave/', views.ProdmastViewSet,name='po_dsd_receive-prodmast-api'),
    path('datas/', views.MergeListViewSet.as_view(), name='po_dsd_receive_merge-list-api'),
    path('validate_po/', views.POViewSet,name='po_dsd_receive-po-api'),
    path('change_pha/', views.changeData,name='change_pha'),
    
]