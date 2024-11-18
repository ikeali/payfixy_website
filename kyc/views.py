
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *

class BusinessDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BusinessDetailsSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(merchant=request.merchant)
            # Update the KYC status
            KYCStatus.objects.update_or_create(merchant=request.merchant, defaults={'completed_business_details': True})
            return Response({'message': 'Business details saved. Continue to Business Documents.'}, status=status.HTTP_201_CREATED)


class BusinessDocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BusinessDocumentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(merchant=request.merchant)
            # Update the KYC status
            KYCStatus.objects.update_or_create(
                merchant=request.merchant, 
                defaults={'completed_business_details': True}
            )
            return Response({'message': 'Business details saved'}, status=status.HTTP_201_CREATED)
        
class BusinessOwnerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BusinessOwnerSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(merchant=request.merchant)
            # Update the KYC status
            KYCStatus.objects.update_or_create(
                merchant=request.merchant, 
                defaults={'completed_business_details': True}
            )
            return Response({'message': 'Business details saved'}, status=status.HTTP_201_CREATED)
        

class KYCSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        merchant = request.user
        serializer = KYCSummarySerializer(merchant)
        return Response(serializer.data)
