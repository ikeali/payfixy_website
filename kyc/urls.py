from django.urls import path, include
from .views import *
from . import views
from rest_framework.routers import DefaultRouter
from .views import BusinessOwnerViewSet

router = DefaultRouter()
router.register(r'business-owner', BusinessOwnerViewSet, basename='business-owner')





urlpatterns = [
    path('', include(router.urls)),
    path("api/verify-bvn", views.verify_bvn, name="verify_bvn"),
    path('business-details/', BusinessDetailsView.as_view(), name='business-details'),
    path('business-documents/', BusinessDocumentView.as_view(), name='business-documents'),
    path('kyc-summary/', KYCSummaryView.as_view(), name='kyc-summary'),

]
