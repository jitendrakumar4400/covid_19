#THIS SCRIPT PROVIDES ALL AVAILABLE SLOTS IN MULPLITE PINCODES OR DISTRICTS FOR VACCINE OF YOUR CHOICE FOR NEXT 30 DAYS FROM COWIN SITE

import requests
from datetime import datetime, timedelta
import time

def get_by_pincode_date(location,pincode_district,date):
    if location == "district":
        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="+str(pincode_district)+"&date=" + str(date)
    elif location == "pincode"
        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode="+str(pincode_district)+"&date="+str(date)
    
    #print(url)
    payload={}
    headers = {
      'Host': 'cdn-api.co-vin.in',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
      'Accept': 'application/json, text/plain, */*',
      'Accept-Language': 'en-US,en;q=0.5',
      'Accept-Encoding': 'gzip, deflate, br',
      'Origin': 'https://www.cowin.gov.in',
      'DNT': '1',
      'Connection': 'keep-alive',
      'Referer': 'https://www.cowin.gov.in/'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    #print(response)
    if response.status_code != 200:
        print(url)
        print(response)
        jsonResponse = {"centers":[]}
        return jsonResponse
        #time.sleep(30)
        #get_by_pincode_date(pincode, date)
    jsonResponse = response.json()
    return jsonResponse

def generate_next_thirty_dates():
    today_date = datetime.today().strftime('%d-%m-%Y')
    thirty_days_array = []
    thirty_days_array.append(today_date)
    for x in [7,14,20]:
        res = (datetime.strptime(today_date, '%d-%m-%Y') + timedelta(days=x)).strftime('%d-%m-%Y')
        thirty_days_array.append(res)
    return thirty_days_array


def parse_cowin_response(res):
    centers = res["centers"]
    if len(centers) > 0:
        for center in centers:
            center_name = center["name"]
            address = center["address"]
            pincode = center["pincode"]
            fee_type = center["fee_type"]
            sessions = center["sessions"]
            for session in sessions:
                
                session_date = session["date"]
                available_capacity = session["available_capacity"]
                min_age_limit = session["min_age_limit"]
                vaccine = session["vaccine"]
                ###PLEASE EDIT FILTER BASED YOUR NEEDS
                #if available_capacity > 0  and fee_type != "Free":
                if available_capacity > 0 and vaccine != "COVISHIELD":
                    result = center_name+","+address+","+fee_type+","+str(pincode)+","+session_date+","+str(available_capacity)+","+str(min_age_limit)+","+vaccine
                    print(result)
                    


# Provide array of pincodes or District IDs as numeric array
pincode_distict_array=[]
#Provide either "district" or "pincode"
location=""
date_array=generate_next_thirty_dates()
print("center_name,address,fee_type,pincode,session_date,available_capacity,min_age_limit,vaccine")
for d in date_array:
     for p in pincode_distict_array:
         response = get_by_pincode_date(p, d)
         parse_cowin_response(response)
         time.sleep(2)


print("***********************")
