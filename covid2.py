from typing import Iterable, Dict, Union, List
from json import dumps
from requests import get
from http import HTTPStatus
import argparse
import sys, os


StructureType = Dict[str, Union[dict, str]]
FiltersType = Iterable[str]
APIResponseType = Union[List[StructureType], str]

ltlaArea=["Aberdeen City","Aberdeenshire","Adur","Allerdale","Amber Valley","Angus","Antrim and Newtownabbey","Ards and North Down","Argyll and Bute","Armagh City, Banbridge and Craigavon","Arun","Ashfield","Ashford","Aylesbury Vale","Babergh","Barking and Dagenham","Barnet","Barnsley","Barrow-in-Furness","Basildon","Basingstoke and Deane","Bassetlaw","Bath and North East Somerset","Bedford","Belfast","Bexley","Birmingham","Blaby","Blackburn with Darwen","Blackpool","Blaenau Gwent","Bolsover","Bolton","Boston","Bournemouth, Christchurch and Poole","Bracknell Forest","Bradford","Braintree","Breckland","Brent","Brentwood","Bridgend","Brighton and Hove","Bristol, City of","Broadland","Bromley","Bromsgrove","Broxbourne","Broxtowe","Burnley","Bury","Caerphilly","Calderdale","Cambridge","Camden","Cannock Chase","Canterbury","Cardiff","Carlisle","Carmarthenshire","Castle Point","Causeway Coast and Glens","Central Bedfordshire","Ceredigion","Charnwood","Chelmsford","Cheltenham","Cherwell","Cheshire East","Cheshire West and Chester","Chesterfield","Chichester","Chiltern","Chorley","City of Edinburgh","Clackmannanshire","Colchester","Conwy","Copeland","Corby","Cornwall and Isles of Scilly","Cotswold","County Durham","Coventry","Craven","Crawley","Croydon","Dacorum","Darlington","Dartford","Daventry","Denbighshire","Derby","Derbyshire Dales","Derry City and Strabane","Doncaster","Dorset","Dover","Dudley","Dumfries and Galloway","Dundee City","Ealing","East Ayrshire","East Cambridgeshire","East Devon","East Dunbartonshire","East Hampshire","East Hertfordshire","East Lindsey","East Lothian","East Northamptonshire","East Renfrewshire","East Riding of Yorkshire","East Staffordshire","East Suffolk","Eastbourne","Eastleigh","Eden","Elmbridge","Enfield","Epping Forest","Epsom and Ewell","Erewash","Exeter","Falkirk","Fareham","Fenland","Fermanagh and Omagh","Fife","Flintshire","Folkestone and Hythe","Forest of Dean","Fylde","Gateshead","Gedling","Glasgow City","Gloucester","Gosport","Gravesham","Great Yarmouth","Greenwich","Guildford","Gwynedd","Hackney and City of London","Halton","Hambleton","Hammersmith and Fulham","Harborough","Haringey","Harlow","Harrogate","Harrow","Hart","Hartlepool","Hastings","Havant","Havering","Herefordshire, County of","Hertsmere","High Peak","Highland","Hillingdon","Hinckley and Bosworth","Horsham","Hounslow","Huntingdonshire","Hyndburn","Inverclyde","Ipswich","Isle of Anglesey","Isle of Wight","Islington","Kensington and Chelsea","Kettering","King's Lynn and West Norfolk","Kingston upon Hull, City of","Kingston upon Thames","Kirklees","Knowsley","Lambeth","Lancaster","Leeds","Leicester","Lewes","Lewisham","Lichfield","Lincoln","Lisburn and Castlereagh","Liverpool","Luton","Maidstone","Maldon","Malvern Hills","Manchester","Mansfield","Medway","Melton","Mendip","Merthyr Tydfil","Merton","Mid Devon","Mid Suffolk","Mid Sussex","Mid Ulster","Mid and East Antrim","Middlesbrough","Midlothian","Milton Keynes","Mole Valley","Monmouthshire","Moray","Na h-Eileanan Siar","Neath Port Talbot","New Forest","Newark and Sherwood","Newcastle upon Tyne","Newcastle-under-Lyme","Newham","Newport","Newry, Mourne and Down","North Ayrshire","North Devon","North East Derbyshire","North East Lincolnshire","North Hertfordshire","North Kesteven","North Lanarkshire","North Lincolnshire","North Norfolk","North Somerset","North Tyneside","North Warwickshire","North West Leicestershire","Northampton","Northumberland","Norwich","Nottingham","Nuneaton and Bedworth","Oadby and Wigston","Oldham","Orkney Islands","Oxford","Pembrokeshire","Pendle","Perth and Kinross","Peterborough","Plymouth","Portsmouth","Powys","Preston","Reading","Redbridge","Redcar and Cleveland","Redditch","Reigate and Banstead","Renfrewshire","Rhondda Cynon Taf","Ribble Valley","Richmond upon Thames","Richmondshire","Rochdale","Rochford","Rossendale","Rother","Rotherham","Rugby","Runnymede","Rushcliffe","Rushmoor","Rutland","Ryedale","Salford","Sandwell","Scarborough","Scottish Borders","Sedgemoor","Sefton","Selby","Sevenoaks","Sheffield","Shetland Islands","Shropshire","Slough","Solihull","Somerset West and Taunton","South Ayrshire","South Bucks","South Cambridgeshire","South Derbyshire","South Gloucestershire","South Hams","South Holland","South Kesteven","South Lakeland","South Lanarkshire","South Norfolk","South Northamptonshire","South Oxfordshire","South Ribble","South Somerset","South Staffordshire","South Tyneside","Southampton","Southend-on-Sea","Southwark","Spelthorne","St Albans","St. Helens","Stafford","Staffordshire Moorlands","Stevenage","Stirling","Stockport","Stockton-on-Tees","Stoke-on-Trent","Stratford-on-Avon","Stroud","Sunderland","Surrey Heath","Sutton","Swale","Swansea","Swindon","Tameside","Tamworth","Tandridge","Teignbridge","Telford and Wrekin","Tendring","Test Valley","Tewkesbury","Thanet","Three Rivers","Thurrock","Tonbridge and Malling","Torbay","Torfaen","Torridge","Tower Hamlets","Trafford","Tunbridge Wells","Uttlesford","Vale of Glamorgan","Vale of White Horse","Wakefield","Walsall","Waltham Forest","Wandsworth","Warrington","Warwick","Watford","Waverley","Wealden","Wellingborough","Welwyn Hatfield","West Berkshire","West Devon","West Dunbartonshire","West Lancashire","West Lindsey","West Lothian","West Oxfordshire","West Suffolk","Westminster","Wigan","Wiltshire","Winchester","Windsor and Maidenhead","Wirral","Woking","Wokingham","Wolverhampton","Worcester","Worthing","Wrexham","Wychavon","Wycombe","Wyre","Wyre Forest","York"]

def get_paginated_dataset(filters: FiltersType, structure: StructureType,
                          as_csv: bool = False) -> APIResponseType:
    """
    Extracts paginated data by requesting all of the pages
    and combining the results.

    Parameters
    ----------
    filters: Iterable[str]
        API filters. See the API documentations for additional
        information.

    structure: Dict[str, Union[dict, str]]
        Structure parameter. See the API documentations for
        additional information.

    as_csv: bool
        Return the data as CSV. [default: ``False``]

    Returns
    -------
    Union[List[StructureType], str]
        Comprehensive list of dictionaries containing all the data for
        the given ``filters`` and ``structure``.
    """
    endpoint = "https://api.coronavirus.data.gov.uk/v1/data"

    api_params = {
        "filters": str.join(";", filters),
        "structure": dumps(structure, separators=(",", ":")),
        "format": "json" if not as_csv else "csv"
    }
    
    print(api_params.get("filters"))

    data = list()

    page_number = 1

    while True:
        # Adding page number to query params
        api_params["page"] = page_number

        response = get(endpoint, params=api_params, timeout=10)

        if response.status_code >= HTTPStatus.BAD_REQUEST:
            raise RuntimeError(f'Request failed: {response.text}')
        elif response.status_code == HTTPStatus.NO_CONTENT:
            break

        if as_csv:
            csv_content = response.content.decode()

            # Removing CSV header (column names) where page 
            # number is greater than 1.
            if page_number > 1:
                data_lines = csv_content.split("\n")[1:]
                csv_content = str.join("\n", data_lines)

            data.append(csv_content.strip())
            page_number += 1
            continue

        current_data = response.json()
        page_data: List[StructureType] = current_data['data']
        
        data.extend(page_data)

        # The "next" attribute in "pagination" will be `None`
        # when we reach the end.
        if current_data["pagination"]["next"] is None:
            break

        page_number += 1

    if not as_csv:
        return data

    # Concatenating CSV pages
    return str.join("\n", data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--area', help='Give a place name in England to highlight the result in history, eg. Oxford')
    parser.add_argument('--type', default='ltla', help='Option, give a area type, ltla, utla, region, or nation')
    parser.add_argument('value', metavar='N', type=int, nargs='?', default=10,
                    help="an integer for showing the days in history")

    args = parser.parse_args()

    query_filters = [
        f"areaType="+ args.type.lower(),  #region"  #utla #nation or ltla
    ]

    if args.area !=None:
        for e in ltlaArea:
            if args.area in e:
                print("Will try to show history results for {} if it exists".format(args.area))
                query_filters.append(f"areaName="+e)
                break
        #print("Will try to show history results for {} if it exists".format(args.area))
        #query_filters.append(f"areaName="+args.area)

        #f"areaName="+args.area #example: Oxford", "Windsor and Maidenhead"
        #f"areaCode=E06000040"  #Search from area code York:E06000014, 
        #f"areaCode=E06000040" #E02003426"  #E06000036 Bracknell
        #f"areaName=Bracknell Forest"


    query_structure = {
        "date": "date",
        "name": "areaName",
        "code": "areaCode",
        "daily": "newCasesBySpecimenDate",
        "cumulative": "cumCasesBySpecimenDate"
    }

    '''
    json_data = get_paginated_dataset(query_filters, query_structure)
    print("JSON:")
    print(f"Length:", len(json_data))
    print("Data (first 3 items):", json_data[:5])
    '''
    print("---" * 10)
    csv_data=""
    try:
        csv_data = get_paginated_dataset(query_filters, query_structure, as_csv=True)
        csv_lines = csv_data.split("\n")
    except:
        print("Possiblly server error. Try it late")
        sys.exit()
        
    if len(csv_lines)< 2:
        print("Can not find data for the area " + args.area)
        print("Go to https://coronavirus.data.gov.uk/cases to find the area name covered")
        sys.exit()
    l = args.value+1
    if l > len(csv_lines):
        l= len(csv_lines)
    for e in csv_lines[:l]:
        l = e.split(',')
        if len(l) == 5:
            print('{:12} {:24} {:12} {:7} {:7}'.format(l[0], l[1], l[2],l[3], l[4]))
        else:
            print(e)
        