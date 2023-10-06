import requests
from credentials import CLIENT_ID, CLIENT_SECRET

UPLOAD_URL = "https://www.strava.com/api/v3/uploads"
AUTH_URL = "https://www.strava.com/oauth/token"


def make_post_request(
        url: str,
        headers: dict = None,
        data: dict = None,
        json_data: dict = None,
        params: dict = None,
        files: dict = None) -> dict:
    """
    Wrapper around requests.post method, raising http error code exceptions if the request failed
    :param url: Endpoint URL
    :param headers: Request headers
    :param data: Request data
    :param json_data: Request data in json format
    :param params: Request params
    :param files: Request files
    :return: response json
    """
    try:
        response = requests.post(url, headers=headers, data=data, json=json_data, params=params, files=files)
        response.raise_for_status()
        response_json = response.json()
        return response_json.get("data") if response_json.get("data") else response_json
    except requests.exceptions.HTTPError as http_error:
        if response.status_code == 400:
            print(f"Bad request: {url}")
            raise http_error
        elif response.status_code == 401:
            print(f"Unauthorized: {url}")
            raise http_error
        elif response.status_code == 403:
            print(f"Forbidden: {url}")
            raise http_error
        elif response.status_code == 404:
            print(f"Not found: {url}")
            raise http_error
        elif response.status_code == 429:
            print(f"Too many requests: {url}")
            raise http_error
        elif response.status_code == 500:
            print(f"Internal server error: {url}")
            raise http_error
        elif response.status_code == 503:
            print(f"Service unavailable: {url}")
            raise http_error
        else:
            print("Error:", http_error)
            raise http_error


def get_token(code: str) -> str:
    """
    Gets an access token from Strava
    :param code: Authorization code
    :return: Access token
    """
    try:
        response = make_post_request(
            url=AUTH_URL,
            params={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code"
            }
        )
        return response["access_token"]
    except requests.exceptions.HTTPError as e:
        raise e


def upload_activity(
        token: str,
        file: str,
        name: str,
        sport_type: str = "WeightTraining",
        data_type: str = "tcx") -> dict:
    """
    Uploads a file to Strava
    :param token: Access token
    :param file: Path to file
    :param name: Name of activity
    :param sport_type: Type of sport
    :param data_type: Type of data
    :return: Response json
    """
    try:
        response = make_post_request(
            url=UPLOAD_URL,
            headers={
                "Authorization": f"Bearer {token}"
            },
            params={
                "name": name,
                "sport_type": sport_type,
                "data_type": data_type
            },
            files={
                "file": (file, open(file, "rb"))
            }
        )
        return response
    except requests.exceptions.HTTPError as e:
        raise e
