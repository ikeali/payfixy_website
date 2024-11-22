import json
from rest_framework import status,viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from kyc.tasks import verify_bvn_and_dob


class BusinessDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BusinessDetailsSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(merchant=request.user)
            # Update the KYC status
            KYCStatus.objects.update_or_create(
                merchant=request.user,
                defaults={'completed_business_details': True}
            )
            return Response(
                {'message': 'Business details saved. Continue to Business Documents.'},
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )



class BusinessDocumentView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


    def post(self, request):
        print(request.data)

        serializer = BusinessDocumentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(merchant=request.user)
            # Update the KYC status
            KYCStatus.objects.update_or_create(
                merchant=request.user, 
                defaults={'completed_business_document': True}
            )
            return Response(
                {'message': 'Business document saved. Continue to Bank account.'},
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
        




def verify_bvn(request):
    if request.method == "POST":
        data = json.loads(request.body)
        bvnNumber = data.get("bvnNumber")
        firstname = data.get("firstname")
        lastname = data.get("lastname")

        # Call the verification task
        task_result = verify_bvn_and_dob(bvnNumber, firstname, lastname)
        
        if task_result["status"] == "success" and task_result["data"]["verified"]:
            return JsonResponse({"status": "success", "message": "BVN verified successfully!", "data": task_result["data"]})
        else:
            return JsonResponse({"status": "failure", "message": "BVN verification failed.", "error": task_result["error"]})
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)



class BusinessOwnerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing BusinessOwner records.
    Allows each user to access only their own records.
    """
    serializer_class = BusinessOwnerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return only the records belonging to the authenticated user.
        """
        return BusinessOwner.objects.filter(merchant=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Override the create method to set the merchant and update KYC status.
        """
        serializer = self.get_serializer(data=request.data)
        # print(serializer)
        
        if serializer.is_valid():
            # Save the business owner with the authenticated user as the merchant
            serializer.save(merchant=request.user)
            
            
            # Update or create KYC status for the merchant
            KYCStatus.objects.update_or_create(
                merchant=request.user, 
                defaults={'completed_business_owner': True}
            )
            
            # Return success response
            return Response({'message': 'Business owner saved', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        
        # Return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KYCSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        merchant = request.user
        serializer = KYCSummarySerializer(merchant)
        return Response(serializer.data)
