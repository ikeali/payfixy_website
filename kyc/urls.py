from django.urls import path, include
from .views import *
from . import views
from rest_framework.routers import DefaultRouter
from .views import BusinessOwnerViewSet

router = DefaultRouter()
router.register(r'start_kyc', KYCViewSet, basename='start_kyc')
router.register(r'kyc-review', KYCReviewViewSet, basename='kyc-review')




urlpatterns = [
    path('', include(router.urls)),
    path('business-details/<uuid:uuid>/', BusinessDetailsView.as_view(), name='business-details'),
    path('business-documents/<uuid:uuid>/', BusinessDocumentView.as_view(), name='business-documents'),
    path('business-owner/<uuid:uuid>/', BusinessOwnerViewSet.as_view({'get': 'list', 'post': 'create'}), name='business-owner'),
    # path('bank_account/', BankAccountView.as_view(), name='bank_account'),
    path('verify_account_number/', VerifyAccountNumberView.as_view(), name='account_number'),
    path('verify-bvn/', VerifyBVNView.as_view(), name="verify_bvn"),
]
