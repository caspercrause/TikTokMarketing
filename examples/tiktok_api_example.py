import os
import sys
from datetime import datetime, timedelta
import json

# Add the parent directory to Python path to allow relative imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from src.TikTokMarketing import TikTokAPI, InterestCategories

def print_response(title, response):
    """Helper function to pretty print API responses"""
    print(f"\n{title}")
    print("-" * 50)
    if response and response.get('code') == 0:
        print(json.dumps(response.get('data', {}), indent=2))
    else:
        print(f"Error: {response.get('message') if response else 'No response'}")

def main():
    # Replace with your actual access token and advertiser ID
    access_token = "YOUR_ACCESS_TOKEN"
    advertiser_id = "YOUR_ADVERTISER_ID"
    
    # Initialize the API
    api = TikTokAPI(access_token)
    
    # Set up date range
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    # Test basic reporting
    print_response(
        "Basic Reporting (Advertiser Level)",
        api.get_data(
            start_date=start_date,
            end_date=end_date,
            dimensions=['advertiser_id', 'stat_time_day'],
            metrics=['spend', 'impressions', 'clicks'],
            advertiser_id=advertiser_id,
            data_level='AUCTION_ADVERTISER'
        )
    )
    
    # Test audience reporting by age
    print_response(
        "Audience Reporting (Age Distribution, Sorted by Spend)",
        api.get_data(
            start_date=start_date,
            end_date=end_date,
            dimensions=['age'],
            metrics=['spend', 'impressions', 'clicks'],
            advertiser_id=advertiser_id,
            data_level='AUCTION_ADVERTISER',
            report_type='AUDIENCE',
            audience_dimensions=['age'],
            order_field='spend',
            order_type='ASC'
        )
    )
    
    # Test audience reporting by gender and age
    print_response(
        "Audience Reporting (Gender and Age Distribution)",
        api.get_data(
            start_date=start_date,
            end_date=end_date,
            dimensions=['gender', 'age', 'stat_time_day'],
            metrics=['spend', 'impressions', 'reach'],
            advertiser_id=advertiser_id,
            data_level='AUCTION_ADVERTISER',
            report_type='AUDIENCE',
            audience_dimensions=['gender', 'age']
        )
    )
    
    # Test audience reporting by country
    print_response(
        "Audience Reporting (Top Countries by Impressions)",
        api.get_data(
            start_date=start_date,
            end_date=end_date,
            dimensions=['country_code'],
            metrics=['impressions', 'reach', 'spend'],
            advertiser_id=advertiser_id,
            data_level='AUCTION_ADVERTISER',
            report_type='AUDIENCE',
            audience_dimensions=['country_code'],
            order_field='impressions',
            order_type='DESC'
        )
    )
    
    # Test audience reporting by audience network (ac)
    print_response(
        "Audience Reporting (Audience Network Distribution)",
        api.get_data(
            start_date=start_date,
            end_date=end_date,
            dimensions=['ac'],
            metrics=['impressions', 'reach', 'spend'],
            advertiser_id=advertiser_id,
            data_level='AUCTION_ADVERTISER',
            report_type='AUDIENCE',
            audience_dimensions=['ac'],
            order_field='impressions',
            order_type='DESC'
        )
    )
    
    # Test audience reporting by interest category
    print_response(
        "Audience Reporting (Interest Categories, Sorted by Impressions)",
        InterestCategories.map_response(api.get_data(
            start_date=start_date,
            end_date=end_date,
            dimensions=['interest_category'],
            metrics=['impressions', 'reach', 'spend', 'clicks'],
            advertiser_id=advertiser_id,
            data_level='AUCTION_ADVERTISER',
            report_type='AUDIENCE',
            audience_dimensions=['interest_category'],
            order_field='impressions',
            order_type='DESC'
        ))
    )

if __name__ == "__main__":
    main() 