import requests
import json
import logging

class TikTokAPI:
    ALLOWED_DATA_LEVELS = {'AUCTION_ADVERTISER', 'AUCTION_CAMPAIGN', 'AUCTION_ADGROUP', 'AUCTION_AD'}

    def __init__(self, access_token):
        self.base_url = 'https://business-api.tiktok.com/open_api/'
        self.endpoint = 'v1.3/report/integrated/get/'
        self.headers = {
            'access-token': access_token,
            'content_type': 'application/json'
        }
        self.logger = logging.getLogger(__name__)

    def get_data(self, start_date, end_date, dimensions, metrics, advertiser_id, data_level):
        if data_level not in self.ALLOWED_DATA_LEVELS:
            raise ValueError("Invalid data_level. Must be one of: AUCTION_ADVERTISER, AUCTION_CAMPAIGN, AUCTION_ADGROUP, AUCTION_AD")
        
        request_url = self.base_url + self.endpoint
        try:
            data = {
                'advertiser_id': advertiser_id,
                'data_level': data_level,
                'report_type': 'BASIC',
                'dimensions': json.dumps(dimensions),
                'metrics': json.dumps(metrics),
                'start_date': start_date,
                'end_date': end_date,
                'lifetime': 'false',
                'page_size': 1000,
            }
            resp = requests.get(request_url, headers=self.headers, data=data)
            resp.raise_for_status()  # Raise error for non-200 responses
            result = resp.json()
            return result
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to decode JSON: {e}")
            return None

    def set_logging_level(self, level):
        self.logger.setLevel(level)

    @staticmethod
    def create_dict(input_list):
        """
        Creates a dict with an empty list of values but assigns the keys from a list of names provided by the user.
        """
        return {key: [] for key in input_list}