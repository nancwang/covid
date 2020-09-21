# covid

The app is used to track latest hotspots/clusters of covid 19 cases in UK only and the data is fetched from https://coronavirus.data.gov.uk/cases.
To get the latest data, please use covid2.py. The link from covid.py will not fetch latest data. It might still work with history data.

Usage for covid2.py:

Sameple of usage:
>python covid2.py --area "Windsor and Maidenhead" 14
will print out the data in latest 14 days for Windsor and Maidenhead

>python covid2.py -h
usage: covid2.py [-h] [--area AREA] [--type TYPE] [N]

positional arguments:
  N            an integer for showing the days in history

optional arguments:
  -h, --help   show this help message and exit
  --area AREA  Give a place name in UK to highlight the result in
               history, eg. Oxford or Edinburgh
  --type TYPE  Option, give a area type, ltla, utla, region, or nation



For covid.py, this is out of dated script which only fetch data from 
 https://coronavirus.data.gov.uk/#category=ltlas&map=case&area=e07000216. The data file will not be updated and not sure how long this data file will be kept.
If the data file is still avaliable, here is how touse to get the history json data.

usage 1: 
Find hotspots/clusters
>python covid.py

usage 2: 
Find history
>python covid.py 2

usage 3: 
download data file
>python covid.py 9

usage 4:
Handling data through downloaded file
>python covid.py --fname ./coronavirus-cases_latest.json

