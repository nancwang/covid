from typing import Iterable, Dict, Union, List
from json import dumps
from requests import get
from http import HTTPStatus
import argparse
import sys, os


StructureType = Dict[str, Union[dict, str]]
FiltersType = Iterable[str]
APIResponseType = Union[List[StructureType], str]


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
        print("Will try to show history results for {} if it exists".format(args.area))
        query_filters.append(f"areaName="+args.area)

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
        