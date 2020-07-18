#!/usr/bin/env python
#
# Very simple Covid 19 cluster tracking for England 
#
# (C)2002-2020 Nancy Wang
#

import sys, os
import json
import pprint
import datetime
import requests
import argparse



class jsonStyle:
    def __init__(self, areas=[], value=6):
        self.areas=areas
        self.value=value
        #print('length of area: ', len(self.areas))

    def metadata(self):
        print("dummy")

    def countries(self, json_data):
        country=json_data['countries']
        print(country[0]['areaName'] + ", record of days:", len(country))

        print('{:14} {} {:5} {:7}'.format('Date', '\t', '  day', '  total'))
        print('{:14} {} {:5} {:7}'.format('----', '\t', '-----', '-------'))
        for e in country:
            #print(e['specimenDate'],e['dailyLabConfirmedCases'])
            print('{:14} {} {:5} {:7}'.format(e['specimenDate'], '\t', e['dailyLabConfirmedCases'], e['totalLabConfirmedCases']))

    def regions(self, json_data):
        #reg_num = 9
        area = json_data['regions']
        dic={}

        for e in area:
            if e['areaCode'] in dic:
                break
            dic[e['areaCode']] = e['areaName']
        
        reg_num = len(dic)

        r=[]
        for e in range(reg_num):
            r.append(area[e]['areaName'])

        for e in range(len(r)):
            print(e, r[e])

        t = int(input("select 0 - 8: "))

        n = 0

        print("Result for " + r[t] +": " )
        print('{:14} {} {:5} {:7}'.format('Date', '\t', '  day', '  total'))
        print('{:14} {} {:5} {:7}'.format('----', '\t', '-----', '-------'))
        for e in range(len(area)):
            if area[e]['areaName'] == r[t]:
                n=n+1
                #print(area[e]['specimenDate'], area[e]['dailyLabConfirmedCases'])
                print('{} {} {:5} {:7}'.format(area[e]['specimenDate'], '\t', area[e]['dailyLabConfirmedCases'], area[e]['totalLabConfirmedCases']))
        print(n)
        #print(r)
    
    def utlas(self, json_data):
        area = json_data['utlas']

        dic={}

        for e in area:
            if e['areaCode'] in dic:
                break
            dic[e['areaCode']] = e['areaName']
        
        reg_num = len(dic)
        r=[]
        for e in range(reg_num):
            r.append(area[e]['areaName'])

        r = sorted(r)
        for e in range(len(r)):
            if e%2 == 1:
                print("{:4} {:35}".format( e, r[e]))
            else:
                print("{:4} {:35}".format( e, r[e]),end='')

        n=0
        s_name=input("\nplease select number for the area or type the name of the area you know: ")
        t=-1

        if s_name.isdigit():
            t=int(s_name)
            if t < len(r) and t> -1:
                s_name=r[t]
                
        print("History result for " + s_name +": " )
        for e in range(len(area)):
            if  s_name.lower() in area[e]['areaName'].lower() : #area[e]['areaName'] == s_name or
                n=n+1
                print(area[e]['specimenDate'], area[e]['dailyLabConfirmedCases'])
        
        print(n)

    def ltlas(self, json_data):
        area = json_data['ltlas']

        dic={}

        for e in area:
            if e['areaCode'] in dic:
                break
            dic[e['areaCode']] = e['areaName']
        
        reg_num = len(dic)
        r=[]
        for e in range(reg_num):
            r.append(area[e]['areaName'])

        r = sorted(r)
        
        for e in range(len(r)):
            if e%2 == 1:
                print("{:4} {:35}".format( e, r[e]))
            else:
                print("{:4} {:35}".format( e, r[e]),end='')

        n=0
        s_name=input("\nplease select number for the area or type the name of area you know: ")
        t=-1

        if s_name.isdigit():
            t=int(s_name)
            if t < len(r) and t> -1:
                s_name=r[t]
                
        print("History result for " + s_name +": " )
        for e in range(len(area)):
            if  s_name.lower() in area[e]['areaName'].lower() : #area[e]['areaName'] == s_name or
                n=n+1
                print(area[e]['areaName'],area[e]['specimenDate'], area[e]['dailyLabConfirmedCases'])
        
        print(n)


    def topList(self, json_data):
        area = json_data['ltlas']
        dic={}

        for e in area:
            if e['areaCode'] in dic:
                break
            dic[e['areaCode']] = e['areaName']

        print(len(dic))
        for e in dic:
            print(dic[e], end='; ')

        print()
        n=0 

        min =int(input("Enter minimum: "))
        for e in range(len(dic)):
            if int(area[e]['dailyLabConfirmedCases']) >= min:
                print(area[e]['specimenDate'], area[e]['areaName'], area[e]['dailyLabConfirmedCases'])


        '''
        t=input("type area name: ")

        print("Result for " + t +": " )
        for e in range(len(area)):
            if t.lower() in area[e]['areaName'].lower() :
                n=n+1
                print(area[e]['specimenDate'], area[e]['dailyLabConfirmedCases'])

        print(n)
        '''

    def hotSpots(self, json_data):
        area = json_data['regions']
        ltlas = json_data['ltlas']
        
        '''dic={}

        for e in area:
            if e['areaCode'] in dic:
                break
            dic[e['areaCode']] = e['areaName']

        #print(len(dic))'''
        
        num_d = int(input("Enter num of day: "))
        if num_d < 1:
            sys.exit()
        today = datetime.datetime.now()
        d=datetime.timedelta(days=num_d)
        day=today - d
        ndayago = day.date().strftime('%Y-%m-%d')
        print("Will check from " + ndayago + " to " + today.date().strftime('%Y-%m-%d'))
        min =int(input("Enter minimum cases: "))
        temp=""
        day_total=0
        
        print('{} {:35} {:5} {:7}'.format('\t', 'Area Name', '  Day', '  Total'))
        print('{} {:35} {:5} {:7}'.format('\t', '---------', '-----', '-------'))
        for e in range(len(area)):
            day_total=day_total+area[e]['dailyLabConfirmedCases']
            if area[e]['specimenDate'] >= ndayago:
                if temp != area[e]['specimenDate']:
                    temp = area[e]['specimenDate']
                    print("Day total = ", day_total)
                    day_total=0
                    print(temp)
                if int(area[e]['dailyLabConfirmedCases']) >= min:
                    if len(self.areas) == 0 or self.containTheAreas(area[e]['areaName']):
                        print('{} {:35} {:5} {:7}'.format('\t', area[e]['areaName'], area[e]['dailyLabConfirmedCases'], area[e]['totalLabConfirmedCases']))
            else:
                print("Day total = ", day_total)
                day_total=0
                break

        print("\nFurther narrow down (ltlas):")

        for e in range(len(ltlas)):
            day_total=day_total+ltlas[e]['dailyLabConfirmedCases']
            if ltlas[e]['specimenDate'] >= ndayago:
                if temp != ltlas[e]['specimenDate']:
                    temp = ltlas[e]['specimenDate']
                    print("Day total = ", day_total)
                    day_total=0
                    print(temp)
                    print('{} {:35} {:3} {:7}'.format('\t', 'Area Name', 'Day', '  Total'))
                    print('{} {:35} {:3} {:7}'.format('\t', '---------', '---', '-------'))
                if int(ltlas[e]['dailyLabConfirmedCases']) >= min:
                    if len(self.areas) == 0 or self.containTheAreas(ltlas[e]['areaName']):
                        print('{} {:35} {:3} {:7}'.format('\t', ltlas[e]['areaName'], ltlas[e]['dailyLabConfirmedCases'], ltlas[e]['totalLabConfirmedCases']))
            else:
                print("Day total = ", day_total)
                day_total=0
                break

    def containTheAreas(self,areaName):
        for e in self.areas:
            if e.lower() in areaName.lower():
                return True
        
        return False

    def jsonFromUrl(self,data,v=6):
        json_data = json.loads(data)

        #pa=["metadata","dailyRecords","ltlas","countries","regions","utlas"]
        options = {2 : "ltlas",
               3 : "countries",
               4 : "regions",
               5 : "utlas",
               6 : "hotSpots",
               7 : "topList",
               8 : 'pprint'}
    
        st=[2,3,4,5,6,7]
        if v not in st:
            for e in options:
                print(e, options[e])
            v=int(input("Select num to run: "))
        if v not in st:
            sys.exit()
        

    
        if v == 2:
            self.ltlas(json_data)
        if v == 3:
            self.countries(json_data)
        if v == 4:
            self.regions(json_data)
        if v == 5:
            self.utlas(json_data)
        if v == 6:
            self.hotSpots(json_data)
        if v == 7:
            self.topList(json_data)
        if v == 8:  # pretty print out
            pprint.pprint(json_data)

 


def xmlfile(fn, st, st2):
    fh=open(fn, 'r')
    lines=fh.readlines()

    #print(fn,st)
    print(lines[0])

    for l in lines :
        if st in l and st2 in l:
            li = l.split(',')
            print(li[3], li[7])

def jsonfile(fn, areas):
    with open(fn, 'r') as f:
        data = f.read()
        json_data = json.loads(data)

    #pa=["metadata","dailyRecords","ltlas","countries","regions","utlas"]
    options = {2 : "ltlas",
               3 : "countries",
               4 : "regions",
               5 : "utlas",
               6 : "hotSpots",
               7 : "hotSpots",
               8 : "pprint"}
    for e in options:
        print(e, options[e])
    
    st='23456'
    v=input("Select num to run: ")
    if v not in st:
        sys.exit()
    
    
    #regions=json_data('regions')
    j=jsonStyle()
    if v == '2':
        j.ltlas(json_data)
    if v == '3':
        j.countries(json_data)
    if v == '4':
        j.regions(json_data)
    if v == '5':
        j.utlas(json_data)
    if v == '6':
        j.hotSpots(json_data)
    if v == '7':
        j.topList(json_data)
    if v == '8':  # pretty print out
        pprint.pprint(json_data)


###### Start from here ############
parser = argparse.ArgumentParser()
parser.add_argument('--area',  action='append', default=[], help='Option, give a place name in England to highlight the result, eg. Windsor')
parser.add_argument('--fname',  help='Option, give a file name either json or cvs')
parser.add_argument('value', metavar='N', type=int, nargs='?', default=6,
                    help="an integer for selection: 2 : ltlas, 3 : countries' 4 : regions, 5 : utlas, 6 : hotSpots, 7 : hotSpots, 8 : pprint")
args = parser.parse_args()



if len(args.area)>0:
    print("Will try to show results for {} if exists".format(args.area))


if args.fname:
    jsonfile(args.fname, args.area, args.value)
else:
    url = 'https://c19downloads.azureedge.net/downloads/json/coronavirus-cases_latest.json'
    r = requests.get(url, allow_redirects=True)

    data = r.content

    j=jsonStyle(args.area,args.value)
    j.jsonFromUrl(data,args.value)
    sys.exit()



'''if len(sys.argv) <2:
    sys.exit()

fn=sys.argv[1]

st=""
if len(sys.argv) >= 3:
    st=sys.argv[2]
st2="Upper"

if len(sys.argv) >= 4:
    st2 = sys.argv[3]

filename, file_extension = os.path.splitext(fn)

if "csv" in file_extension:
    if len(st) > 0:
        xmlfile(fn,st,st2)
elif "json" in file_extension:
    jsonfile(fn)
    '''


