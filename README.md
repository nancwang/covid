# covid

The app is used to track latest hotspots/clusters of covid 19 cases in England only.
The script will go to https://coronavirus.data.gov.uk/#category=ltlas&map=case&area=e07000216 to fetch json data.
A sample file is included

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

