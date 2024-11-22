from celery import shared_task
import requests
from decouple import config
from requests.exceptions import RequestException
from django.core.exceptions import ValidationError
import logging



# Configure logger
logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def verify_bvn_and_dob(self, bvnNumber, firstname, lastname):
    """
    Celery task to verify BVN and DOB using the QoreID API.
    """
    url = f"https://api.qoreid.com/v1/ng/identities/bvn-premium/{bvnNumber}"

    payload = {
        "bvnNumber": bvnNumber,
        "firstname": firstname,
        "lastname": lastname
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {config('QOREID_TOKEN')}"
    }

    try:
        # Make the POST request
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        # Log response for debugging
        logger.info(f"BVN verification response: {response.json()}")

        # Return structured response
        return {
            "status": "success",
            "data": response.json()
        }

    except RequestException as e:
        logger.error(f"BVN verification failed: {str(e)}")

        # Retry if the error is recoverable
        try:
            self.retry(exc=e, countdown=2 ** self.request.retries)
        except self.MaxRetriesExceededError:
            logger.critical("Max retries exceeded for BVN verification.")

        return {
            "status": "failure",
            "error": str(e)
        }
