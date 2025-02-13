# TikTokMarketing [![Latest Version](https://img.shields.io/badge/pypi-0.1.4-blue?&link=https%3A%2F%2Fpypi.org%2Fproject%2Fgoogleadsquerytool%2F)](https://pypi.org/project/TikTokMarketing/)

This package enables efficient querying and retrieval of performance metrics from the TikTok Marketing API on different levels of granularity.

## Build status
![Build Status](https://img.shields.io/badge/build-passing-brightgreen?label=build&color=lime)

## Requirements
 - Python 3.8+

## Installation
```
pip install TikTokMarketing
```

## Features
 - Distributed via PyPI.
 - Wrapper around the TikTok Marketing API to assist marketers on a budget with their reporting.
 - Under the hood `TikTokMarketing` makes use of the `requests` and `json` modules.
 - It has no additional dependencies.
 - `TikTokMarketing` supports the latest version of the API `v1.3`
 - Supports both basic and audience reporting
 - Includes human-readable interest category mapping

## Data Levels

The API returns data on 4 distinct levels:

1. AUCTION_ADVERTISER
2. AUCTION_CAMPAIGN
3. AUCTION_ADGROUP
4. AUCTION_AD

For available dimensions and metrics, refer to the official documentation:
 - [Dimensions](https://ads.tiktok.com/marketing_api/docs?id=1751443956638721)
 - [Metrics](https://ads.tiktok.com/marketing_api/docs?id=1751443967255553)

## Example Usage

### Basic Setup
```python
from TikTokMarketing import TikTokAPI, InterestCategories
from datetime import datetime, timedelta

# Initialize the API
api = TikTokAPI('YOUR_ACCESS_TOKEN')

# Set up date range
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
```

### Basic Reporting
```python
# Basic reporting at advertiser level
basic_result = api.get_data(
    start_date=start_date,
    end_date=end_date,
    dimensions=['advertiser_id', 'stat_time_day'],
    metrics=['spend', 'impressions', 'clicks'],
    advertiser_id='YOUR_ADVERTISER_ID',
    data_level='AUCTION_ADVERTISER'
)
```

### Audience Reporting

#### Age Distribution
```python
age_result = api.get_data(
    start_date=start_date,
    end_date=end_date,
    dimensions=['age'],
    metrics=['spend', 'impressions', 'clicks'],
    advertiser_id='YOUR_ADVERTISER_ID',
    data_level='AUCTION_ADVERTISER',
    report_type='AUDIENCE',
    audience_dimensions=['age'],
    order_field='spend',
    order_type='ASC'
)
```

#### Gender and Age Combined
```python
gender_age_result = api.get_data(
    start_date=start_date,
    end_date=end_date,
    dimensions=['gender', 'age', 'stat_time_day'],
    metrics=['spend', 'impressions', 'reach'],
    advertiser_id='YOUR_ADVERTISER_ID',
    data_level='AUCTION_ADVERTISER',
    report_type='AUDIENCE',
    audience_dimensions=['gender', 'age']
)
```

#### Geographic Distribution
```python
country_result = api.get_data(
    start_date=start_date,
    end_date=end_date,
    dimensions=['country_code'],
    metrics=['impressions', 'reach', 'spend'],
    advertiser_id='YOUR_ADVERTISER_ID',
    data_level='AUCTION_ADVERTISER',
    report_type='AUDIENCE',
    audience_dimensions=['country_code'],
    order_field='impressions',
    order_type='DESC'
)
```

#### Audience Network Analysis
```python
network_result = api.get_data(
    start_date=start_date,
    end_date=end_date,
    dimensions=['ac'],
    metrics=['impressions', 'reach', 'spend'],
    advertiser_id='YOUR_ADVERTISER_ID',
    data_level='AUCTION_ADVERTISER',
    report_type='AUDIENCE',
    audience_dimensions=['ac'],
    order_field='impressions',
    order_type='DESC'
)
```

#### Interest Categories
```python
# Get and map interest categories
interest_result = InterestCategories.map_response(
    api.get_data(
        start_date=start_date,
        end_date=end_date,
        dimensions=['interest_category'],
        metrics=['impressions', 'reach', 'spend', 'clicks'],
        advertiser_id='YOUR_ADVERTISER_ID',
        data_level='AUCTION_ADVERTISER',
        report_type='AUDIENCE',
        audience_dimensions=['interest_category'],
        order_field='impressions',
        order_type='DESC'
    )
)
```

### Converting Results to Pandas DataFrame
```python
import pandas as pd

# Create empty dictionary with column names
dimensions = ['stat_time_day', 'advertiser_id']
metrics = ['spend', 'impressions', 'clicks']
all_fields = dimensions + metrics

TikTok_Data = TikTokAPI.create_dict(input_list=all_fields)

# Populate dictionary from API response
result_list = basic_result.get('data', {}).get('list', [])
for entry in result_list:
    for fieldname in TikTok_Data.keys():
        if fieldname in entry.get('dimensions', {}):
            TikTok_Data[fieldname].append(entry['dimensions'][fieldname])
        else:
            TikTok_Data[fieldname].append(entry['metrics'][fieldname])

# Convert to DataFrame
df = pd.DataFrame(TikTok_Data)
```

## Note
When running `TikTokMarketing` in a docker container, the `ip address` might be blocked with the API response: `Client IP address is in banned Country list`

## Available Parameters

### Report Types
- BASIC
- AUDIENCE

### Audience Dimensions
- gender
- age
- country_code
- ac (Audience network)
- platform
- interest_category
- language
- device_brand
- device_model
- device_price
- network

### Order Types
- ASC
- DESC
