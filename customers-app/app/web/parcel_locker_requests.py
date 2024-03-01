import httpx
import logging

logging.basicConfig(level=logging.INFO)


def test():
    """
    Function to test request with httpx
    """
    return httpx.get('http://nginx-parcel-lockers:80/test')


def get_available_locker(parcel_locker_category_id: int, address_id: int) -> dict:
    """
    Function makes a request to get available locker with given category id and address id and returns the locker.
    """
    try:
        url = f'http://nginx-parcel-lockers:80/parcel_lockers/category/{parcel_locker_category_id}/address/{address_id}'
        response = httpx.get(url)
        response.raise_for_status()  # Raise an error for bad status codes (4xx or 5xx)
        return response.json()
    except httpx.RequestError as req_err:
        raise httpx.RequestError(f"Request error occurred: {req_err}")
    except httpx.TimeoutException as timeout_err:
        raise httpx.TimeoutException(f"Timeout error occurred: {timeout_err}")
    except httpx.HTTPStatusError as status_err:
        logging.error(f"HTTP status error occurred: {status_err}")
        raise httpx.HTTPStatusError(f"HTTP status error occurred: {status_err}",
                                    request=status_err.request, response=status_err.response)
    except Exception as err:
        raise Exception(f"An unexpected error occurred: {err}")
