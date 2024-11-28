import json
from rest_framework import status,viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *



class KYCViewSet(viewsets.ModelViewSet):
    """
    KYC ViewSet to manage the entire KYC process.
    Allows each user to access only their own records.
    """
    serializer_class = KYCSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return KYC.objects.filter(merchant=self.request.user)

    def create(self, request, *args, **kwargs):
        # Handle creating KYC record
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(merchant=request.user)
            return Response({
                'status_code': status.HTTP_201_CREATED,
                'message': 'KYC created',
                'data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Retrieve or create a KYC instance for the current user
        kyc, created = KYC.objects.get_or_create(
            merchant=request.user,
            defaults={'status': 'In Progress'}
        )

        # Add the KYC instance to the request data
        data = request.data.copy()
        data['kyc'] = kyc.id

        # Validate the serializer with the updated data
        serializer = BusinessDetailsSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            kyc.status = "In Progress"
            kyc.save()

            return Response(
                {
                    'status_code': status.HTTP_201_CREATED,
                    'message': 'Business details saved. Continue to Business Documents.',
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
        # Retrieve or create a KYC instance for the current user
        kyc, created = KYC.objects.get_or_create(
            merchant=request.user,
            defaults={'status': 'In Progress'}
        )

        # Add the KYC instance to the request data
        data = request.data.copy()
        data['kyc'] = kyc.id

        # Validate the serializer with the updated data
        serializer = BusinessDocumentSerializer(data=data)

        if serializer.is_valid():
            serializer.save()  # Save the business document

            # Update the KYC status
            kyc.status = "In Progress"
            kyc.save()

            return Response(
                {
                    'status_code': status.HTTP_201_CREATED,
                    'message': 'Business document saved. Continue to Bank account.',
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



# class BankAccountView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         """
#         Handle the creation of a BankAccount entry linked to the authenticated user's KYC.
#         """
#         # Retrieve or create the KYC instance for the current user
#         kyc, created = KYC.objects.get_or_create(
#             merchant=request.user,
#             defaults={'status': 'In Progress'}
#         )

#         # Include the `kyc` reference in the request data
#         data = request.data.copy()
#         data['kyc'] = kyc.id

#         # Validate and save the data using the serializer
#         serializer = BankAccountSerializer(data=data)

#         if serializer.is_valid():
#             serializer.save()  # Save the bank account entry

#             # Update the KYC status
#             kyc.status = "In Progress"  # Optional: Adjust the KYC status if needed
#             kyc.save()

#             return Response(
#                 {
#                     'status_code': status.HTTP_201_CREATED,
#                     'message': 'Bank account saved. Proceed to the next step.',
#                     'data': serializer.data
#                 },
#                 status=status.HTTP_201_CREATED
#             )

#         # Return an error response if validation fails
#         return Response(
#             {
#                 "status_code": status.HTTP_400_BAD_REQUEST,
#                 "error": "Invalid data provided.",
#                 "details": serializer.errors,
#             },
#             status=status.HTTP_400_BAD_REQUEST,
#         )



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
       
       # Retrieve or create a KYC instance for the current user
        kyc, created = KYC.objects.get_or_create(
            merchant=request.user,
            defaults={'status': 'In Progress'}
        )

        # Add the KYC instance to the request data
        data = request.data.copy()
        data['kyc'] = kyc.id

       
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            
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


class KYCReviewViewSet(viewsets.ViewSet):
    """
    Viewset to get a summary of all KYC steps filled so far.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        kyc = KYC.objects.get(merchant=request.user, status='In Progress')
        business_details = BusinessDetails.objects.filter(kyc=kyc)
        business_documents = BusinessDocument.objects.filter(kyc=kyc)
        # bank_account = BankAccount.objects.filter(kyc=kyc)
        business_owner = BusinessOwner.objects.filter(kyc=kyc)

        return Response({
            'business_details': BusinessDetailsSerializer(business_details, many=True).data,
            'business_documents': BusinessDocumentSerializer(business_documents, many=True).data,
            # 'bank_account': BankAccountSerializer(bank_account, many=True).data,
            'business_owner': BusinessOwnerSerializer(business_owner, many=True).data
        })
    
    @action(detail=False, methods=['post'], url_path='submit')
    def submit(self, request, *args, **kwargs):
        """
        Mark the KYC as completed after reviewing all steps.
        """
        try:
            kyc = KYC.objects.get(merchant=request.user, status='In Progress')
        except KYC.DoesNotExist:
            return Response(
                {'error': 'No KYC in progress for this user.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validate that all steps are completed
        if not all([
            BusinessDetails.objects.filter(kyc=kyc).exists(),
            BusinessDocument.objects.filter(kyc=kyc).exists(),
            # BankAccount.objects.filter(kyc=kyc).exists(),
            BusinessOwner.objects.filter(kyc=kyc).exists()
        ]):
            return Response(
                {'error': 'All KYC steps must be completed before submission.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Mark KYC as completed
        kyc.status = 'Completed'
        kyc.save()

        return Response(
            {'message': 'KYC successfully submitted.'},
            status=status.HTTP_200_OK
        )