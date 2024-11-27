import json
from rest_framework import status,viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
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
            serializer.save(merchant=request.user)
            KYCStatus.objects.update_or_create(
                merchant=request.user,
                defaults={'completed_business_details': True}
            )
            return Response(
                {
                    'status_code': status.HTTP_201_CREATED,
                    'message': 'Business details saved. Continue to Business Documents.'
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "error": "Invalid data provided.",
                "details": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )



class BusinessDocumentView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


    def post(self, request):
        print(request.data)

        serializer = BusinessDocumentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(merchant=request.user)
            KYCStatus.objects.update_or_create(
                merchant=request.user, 
                defaults={'completed_business_document': True}
            )
            return Response(
                {
                    'status_code':status.HTTP_201_CREATED,
                    'message': 'Business document saved. Continue to Bank account.'
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "error": "Invalid data provided.",
                "details": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class VerifyAccountNumberView(APIView):

    def post(self, request, *args, **kwargs):
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')
        accountNumber = request.data.get('accountNumber')
        bankCode = request.data.get('bankCode')

        # Check if required fields are present
        if not all([firstname, lastname, accountNumber, bankCode]):
            return Response(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "error": "Missing required parameters: firstname, lastname, accountNumber, bankCode"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        url = "https://api.qoreid.com/v1/ng/identities/nuban"

        # Prepare the payload with the required fields
        payload = {
            "firstname": firstname,
            "lastname": lastname,
            "accountNumber": accountNumber,
            "bankCode": bankCode
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {config('QOREID_TOKEN')}"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)

            print("Response Status Code:", response.status_code)
            print("Response Content:", response.text)

            if response.status_code == 200:
                data = response.json()
                if data.get("status", {}).get("status") == "verified":
                    return Response({"is_verified": True}, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {   
                            "status_code":status.HTTP_400_BAD_REQUEST,
                            "is_verified": False,
                            "message": "Account verification failed.",
                            "details": data,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                print("Error response status:", response.status_code)
                print("Error response details:", response.json())
                return Response(
                    {"error": "Unable to verify Account number", "details": response.json()},
                    status=response.status_code,
                )

        except Exception as e:
            print("Error occurred during API request:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AccountNumberView(APIView):
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        """
        Override the create method to set the merchant and update KYC status.
        """
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Save the business owner with the authenticated user as the merchant
            serializer.save(merchant=request.user)
            
            
            # Update or create KYC status for the merchant
            KYCStatus.objects.update_or_create(
                merchant=request.user, 
                defaults={'completed_bank_account': True}
            )
            
            return Response({
                'status_code': status.HTTP_201_CREATED,
                'message': 'Bank Account saved', 'data': serializer.data
                },
                status=status.HTTP_201_CREATED)
            
        return Response(
            {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "error": "Invalid data provided.",
                "details": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )





class VerifyBVNView(APIView):
    """
    Endpoint for verifying BVN information.
    """
    def post(self, request, *args, **kwargs):
        bvnNumber = request.data.get("bvnNumber")
        firstname = request.data.get("firstname")
        lastname = request.data.get("lastname")

        if not bvnNumber or not firstname or not lastname:
            return Response({"error": "Missing required fields: bvnNumber, firstname, lastname"}, status=status.HTTP_400_BAD_REQUEST)

        url = f"https://api.qoreid.com/v1/ng/identities/bvn-premium/{bvnNumber}"

        payload = {
            "firstname": firstname,
            "lastname": lastname,
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {config('QOREID_TOKEN')}"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)

            print("Response Status Code:", response.status_code)
            print("Response Content:", response.text)

            if response.status_code == 200:
                data = response.json()
                if data.get("status", {}).get("status") == "verified":
                    return Response({"is_verified": True}, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {
                            "status_code": status.HTTP_400_BAD_REQUEST,
                            "is_verified": False,
                            "message": "BVN verification failed.",
                            "details": data,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "error": "Unable to verify BVN", "details": response.json()
                    },
                    status=response.status_code,
                )

        except Exception as e:
            return Response({
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



    
    def get(self, request, bvn_nuban=None, *args, **kwargs):
        """
        Fetch account information from the external API.
        """
        if not bvn_nuban:
            return Response(
                {"error": "Account number (bvn_nuban) is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        url = f"https://api.qoreid.com/v1/banks/{bvn_nuban}"
        headers = {"accept": "application/json"}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Failed to fetch account information", "details": response.text},
                    status=response.status_code,
                )
        except requests.RequestException as e:
            return Response(
                {"error": "An error occurred while fetching account information", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )





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
        
        if serializer.is_valid():
            serializer.save(merchant=request.user)
            
            
            KYCStatus.objects.update_or_create(
                merchant=request.user, 
                defaults={'completed_business_owner': True}
            )
            
            return Response({
                'status_code': status.HTTP_201_CREATED,
                'message': 'Business owner saved',
                'data': serializer.data
                },
                status=status.HTTP_201_CREATED)
        
        return Response(
            {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "error": "Invalid data provided.",
                "details": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class KYCSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        merchant = request.user
        serializer = KYCSummarySerializer(merchant)
        return Response(serializer.data)
