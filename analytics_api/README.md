##Under Construction
#Analytics APIs
####python version 2.7.5
####bash version 4.1.2(1)
####Purpose: Rerieve analytics report via API
-------------------------------------------------------------------
#####primo analytics api

input = config file in /alma/config/ with:

```
url=https://api-na.hosted.exlibrisgroup.com/primo/v1/analytics/reports
#path=/shared/Primo Emory University/Reports/ACOOPE5/Popular_searches
path=[your report path]
apikey=[your api key]
limit=1000
```
>/alma/bin/primo_analytics_api.py /alma/config/primo_analytics_api.cfg

----------------------------------------------------------------------
