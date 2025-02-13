import requests
import json
import logging

class InterestCategories:
    """Class to handle interest category mappings"""
    
    CATEGORIES_V2 = {
        '10': 'Video & Animation',
        '11': 'Games',
        '12': 'Food & Beverages',
        '13': 'Music',
        '14': 'Learning & Education',
        '15': 'News & Politics',
        '16': 'Business & Finance',
        '17': 'Sports & Outdoors',
        '18': 'Auto & Transportation',
        '19': 'Pets',
        '20': 'Technology',
        '21': 'Travel',
        '22': 'Books & Literature',
        '23': 'Entertainment',
        '24': 'Family & Relationships',
        '25': 'Fitness & Yoga',
        '26': 'Photography',
        '27': 'Home & Garden',
        '28': 'Beauty & Personal Care',
        '30': 'Arts & Crafts'
    }
    
    CATEGORIES_V1 = {
        '101': 'Video & Animation',
        '102': 'Games',
        '103': 'Food & Beverages',
        '104': 'Music',
        '105': 'Learning & Education',
        '106': 'News & Politics',
        '107': 'Business & Finance',
        '108': 'Sports & Outdoors',
        '110': 'Pets',
        '111': 'Technology',
        '113': 'Books & Literature',
        '114': 'Entertainment',
        '116': 'Fitness & Yoga',
        '118': 'Home & Garden',
        '119': 'Beauty & Personal Care'
    }
    
    @classmethod
    def get_name(cls, category_id, version='v2'):
        """
        Maps interest category IDs to human-readable names.
        Reference: https://business-api.tiktok.com/marketing_api/docs?id=1737174886619138
        
        Args:
            category_id: The category ID to look up
            version: Version of categories to use ('v1' or 'v2')
        
        Returns:
            str: The human-readable category name or 'Unknown Category (ID)'
        """
        categories = cls.CATEGORIES_V2 if version == 'v2' else cls.CATEGORIES_V1
        return categories.get(str(category_id), f'Unknown Category ({category_id})')
    
    @classmethod
    def map_response(cls, response):
        """
        Maps interest category IDs to category names in the API response
        
        Args:
            response: The API response to process
            
        Returns:
            dict: The processed response with added category names
        """
        if not response or response.get('code') != 0:
            return response
            
        data = response.get('data', {})
        for item in data.get('list', []):
            if 'dimensions' in item:
                dims = item['dimensions']
                # Map both v1 and v2 categories if present
                if 'interest_category_v2' in dims:
                    item['category_name_v2'] = cls.get_name(
                        dims['interest_category_v2'], 'v2'
                    )
                if 'interest_category' in dims and dims['interest_category']:
                    item['category_name_v1'] = cls.get_name(
                        dims['interest_category'], 'v1'
                    )
        
        return response

class TikTokAPI:
    ALLOWED_DATA_LEVELS = {'AUCTION_ADVERTISER', 'AUCTION_CAMPAIGN', 'AUCTION_ADGROUP', 'AUCTION_AD'}
    ALLOWED_REPORT_TYPES = {'BASIC', 'AUDIENCE'}
    ALLOWED_ORDER_TYPES = {'ASC', 'DESC'}
    ALLOWED_AUDIENCE_DIMENSIONS = {
        'country_code',  # Country code
        'ac',           # Audience network
        'device_brand', # Device brand
        'language',     # Language
        'interest_category',  # Interest categories
        'network',      # Network type
        'device_price', # Device price range
        'age',         # Age groups
        'device_model', # Device model
        'gender',      # Gender
        'platform'     # Platform
    }
    
    def __init__(self, access_token):
        self.base_url = 'https://business-api.tiktok.com/open_api/'
        self.endpoint = 'v1.3/report/integrated/get/'
        self.headers = {
            'access-token': access_token,
            'content_type': 'application/json'
        }
        self.logger = logging.getLogger(__name__)

    def get_data(self, start_date, end_date, metrics, advertiser_id, 
                 data_level, report_type='BASIC', dimensions=None, 
                 audience_dimensions=None, order_field=None, 
                 order_type=None, page=1, page_size=100):
        """
        Get report data from TikTok Marketing API.
        
        Args:
            start_date: Start date for the report (format: 'YYYY-MM-DD')
            end_date: End date for the report (format: 'YYYY-MM-DD')
            metrics: List of metrics to include (e.g., ['spend', 'impressions'])
            advertiser_id: The advertiser ID
            data_level: Level of data aggregation
            report_type: Type of report ('BASIC' or 'AUDIENCE')
            dimensions: List of dimensions to include (e.g., ['country_code', 'stat_time_day'])
            audience_dimensions: List of audience dimensions for AUDIENCE report type
                (must be from: device_price, platform, device_brand, interest_category, 
                age, ac, network, gender, device_model, language)
            order_field: Field to sort by (e.g., 'spend')
            order_type: Sort order ('ASC' or 'DESC')
            page: Page number for pagination (default: 1)
            page_size: Number of items per page (default: 100)
        
        Returns:
            dict: API response containing the requested report data
            None: If the request fails
        
        Raises:
            ValueError: If invalid parameters are provided
        """
        # Validate data level
        if data_level not in self.ALLOWED_DATA_LEVELS:
            raise ValueError(f"Invalid data_level. Must be one of: {', '.join(self.ALLOWED_DATA_LEVELS)}")
            
        # Validate report type
        if report_type not in self.ALLOWED_REPORT_TYPES:
            raise ValueError(f"Invalid report_type. Must be one of: {', '.join(self.ALLOWED_REPORT_TYPES)}")
            
        # Validate audience dimensions for AUDIENCE report type
        if report_type == 'AUDIENCE':
            if not audience_dimensions:
                raise ValueError("audience_dimensions is required when report_type is 'AUDIENCE'")
            invalid_dimensions = set(audience_dimensions) - self.ALLOWED_AUDIENCE_DIMENSIONS
            if invalid_dimensions:
                raise ValueError(f"Invalid audience dimensions: {invalid_dimensions}. "
                               f"Must be from: {', '.join(self.ALLOWED_AUDIENCE_DIMENSIONS)}")
            
        # Validate order type if provided
        if order_type and order_type not in self.ALLOWED_ORDER_TYPES:
            raise ValueError(f"Invalid order_type. Must be one of: {', '.join(self.ALLOWED_ORDER_TYPES)}")
        
        request_url = self.base_url + self.endpoint
        try:
            # Build base request data
            data = {
                'advertiser_id': advertiser_id,
                'service_type': 'AUCTION',
                'data_level': data_level,
                'report_type': report_type,
                'metrics': json.dumps(metrics),
                'start_date': start_date,
                'end_date': end_date,
                'page': page,
                'page_size': page_size,
            }
            
            # Add dimensions if provided
            if dimensions:
                data['dimensions'] = json.dumps(dimensions)
            
            # Add audience dimensions for AUDIENCE report type
            if report_type == 'AUDIENCE':
                data['audience_dimensions'] = json.dumps(audience_dimensions)
            
            # Add sorting parameters if provided
            if order_field:
                data['order_field'] = order_field
                
            if order_type:
                data['order_type'] = order_type
            
            # Make the request
            resp = requests.get(request_url, headers=self.headers, data=data)
            resp.raise_for_status()
            result = resp.json()
            
            # Log warning if response indicates an error
            if result.get('code') != 0:
                self.logger.warning(f"API returned error: {result.get('message')}")
                
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