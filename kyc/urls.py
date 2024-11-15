from django.urls import path
from .views import *

urlpatterns = [
    path('business-details/', BusinessDetailsView.as_view(), name='business-details'),
    path('business-documents/', BusinessDocumentView.as_view(), name='business-documents'),
    path('business-owner/', BusinessOwnerView.as_view(), name='business-owner'),
    path('kyc-summary/', KYCSummaryView.as_view(), name='kyc-summary'),

]
