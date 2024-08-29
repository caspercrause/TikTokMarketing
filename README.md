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


The API returns data on 4 distinct levels:

1. AUCTION_ADVERTISER
1. AUCTION_CAMPAIGN
1. AUCTION_ADGROUP
1. AUCTION_AD

You can pass your own dimensions and metrics as a list:

For a list of these please refer to the official documentation:
 - [Dimensions](https://ads.tiktok.com/marketing_api/docs?id=1751443956638721)
 - [Metrics](https://ads.tiktok.com/marketing_api/docs?id=1751443967255553)

## Example usage

### To query data at the ad level:
```
Data_Level = 'AUCTION_AD'

# Custom Metrics and Dimensions to report on
metrics = [
        'campaign_name', 'adgroup_name', 'ad_name', 'currency', 'spend', 'impressions', 'clicks', 'conversion'
    ]

dimensions = [
    'ad_id' ,'stat_time_day'
]

```

### Querying data at the ad group level:
```
Data_Level = 'AUCTION_ADGROUP'

# Custom Metrics and Dimensions to report on
metrics = [
        'campaign_name', 'adgroup_name', 'currency', 'spend',  'impressions', 'clicks', 'conversion'
    ]

dimensions = [
    'stat_time_day', 'adgroup_id'
]

```

### Querying at the campaign level:

```
Data_Level = 'AUCTION_CAMPAIGN'

# Custom Metrics and Dimensions to report on
metrics = [
        'campaign_name', 'currency', 'spend',  'impressions', 'clicks', 'conversion'
    ]

dimensions = [
    'stat_time_day', 'campaign_id'
]

```

### Querying at the advertiser level:
```
Data_Level = 'AUCTION_ADVERTISER'

# Custom Metrics and Dimensions to report on
metrics = [
       'advertiser_name', 'currency', 'spend',  'impressions', 'clicks', 'conversion'
    ]

dimensions = [
    'stat_time_day', 'advertiser_id'
]
```
### Connecting to the API:
```
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
from TikTokMarketing import TikTokAPI 

tik_tok_advertiser_id = '123344555556667' # Enter advertiser id here

UpperLimit = date.today() # Must be a date object
LowerLimit = UpperLimit - relativedelta(days=30) # Must be a date object
api_service = TikTokAPI('Your API TOKEN HERE')

# Max time span is 30 days.
result = api_service.get_data(
    start_date    = LowerLimit, 
    end_date      = UpperLimit, 
    dimensions    = dimensions, 
    metrics       = metrics,
    advertiser_id = tik_tok_advertiser_id, 
    data_level    = Data_Level)

result_list = result.get('data').get('list')

print(f' *** Processing request id: {result.get("request_id")} ***')

print(f" *** API repsonse: '{result.get('message')}'")

```
### Unpacking the results and creating a pandas dataframe from it:
```

# Iterate through the list : You have two keys -  dimensions and metrics

dimensions.extend(metrics)

TikTok_Data = TikTokAPI.create_dict( input_list=dimensions )

for entry in result_list:
    for fieldname in TikTok_Data.keys():
        # Look for keyname in dimensions
        if fieldname in entry.get('dimensions'):
            TikTok_Data.get(fieldname).append( entry.get('dimensions').get(fieldname) )
        # Then the key must be in metrics
        else:
            TikTok_Data.get(fieldname).append( entry.get('metrics').get(fieldname) )
        

TikTok_Data = pd.DataFrame(TikTok_Data)
```

I have noticed that when trying to run `TikTokMarketing` in a docker containter, the `ip address` is blocked and the API response is `Client IP address is in banned Country list`
