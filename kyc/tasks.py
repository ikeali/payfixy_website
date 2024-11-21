from celery import shared_task
import requests
from decouple import config
from django.core.exceptions import ValidationError
import logging



# Set up logging
logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def verify_bvn_and_dob(self, bvn, first_name, last_name, dob):
    """
    Task to verify BVN and Date of Birth (DOB) using an external API.
    """
    url = f"https://api.qoreid.com/v1/ng/identities/bvn-premium/{bvn}"
    
    headers = {
        "Authorization": f"Bearer {config('COREID_TOKEN')}",
        "Content-Type": "application/json",
    }

    payload = {
        "firstname": first_name,
        "lastname": last_name,
        "date_of_birth": dob  
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()

        # Check if the BVN verification is successful
        if data.get("status") != "verified":
            logger.error(f"BVN verification failed for {bvn}.")
            return {"status": False, "message": "The BVN verification failed."}

        # Check if the Date of Birth matches the response
        verified_dob = data.get("data", {}).get("dob")
        
        # Ensure the DOB is in the correct format
        if isinstance(dob, str):
            dob = dob.strip()
        else:
            dob = dob.strftime('%d-%m-%Y')

        if verified_dob != dob:
            logger.error(f"Date of birth mismatch for {bvn}. Expected {dob}, got {verified_dob}.")
            return {"status": False, "message": "The BVN and Date of Birth do not match."}

        logger.info(f"BVN {bvn} verified successfully.")
        return {"status": True, "message": "BVN verified successfully."}

    except requests.exceptions.RequestException as e:
        # Handle network-related errors (timeouts, connection errors, etc.)
        logger.error(f"Error verifying BVN {bvn}: {str(e)}")
        
        try:
            raise self.retry(exc=e, countdown=30)
        except self.MaxRetriesExceededError:
            logger.error(f"Max retries exceeded for BVN {bvn}.")
            return {"status": False, "message": f"Error verifying BVN: {str(e)}"}

    except Exception as e:
        logger.error(f"Unexpected error during BVN verification for {bvn}: {str(e)}")
        return {"status": False, "message": f"Unexpected error: {str(e)}"}
