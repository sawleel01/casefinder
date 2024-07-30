import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
import json

def fetch_case_details(regno):
    url = 'https://supremecourt.gov.np/lic/sys.php?d=reports&f=case_details'
    headers = {
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://supremecourt.gov.np',
        'Referer': 'https://supremecourt.gov.np/lic/sys.php?d=reports&f=case_details&num=1&mode=view&caseno=215144',
    }
    data = {
        'syy': '',
        'smm': '',
        'sdd': '',
        'mode': 'show',
        'list': 'list',
        'regno': regno,
        'tyy': '',
        'tmm': '',
        'tdd': ''
    }
    
    response = rq.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_case_details(html):
    soup = bs(html, 'lxml')
    table = soup.find('table')
    # print(table)
    
    if not table:
        print("No table found. Full HTML content:")
        print(html)
        return None

    rows = table.find_all('tr')
    # print(rows)
    data = []
    for row in rows:
        cols = row.find_all('td')
        # print(cols)
        cols = [ele.text.strip() for ele in cols]
        if cols: 
            data.append(cols)

    print(f"Parsed data: {data}")
    
    return data

def parse_second_url(html):
    soup = bs(html, 'lxml')
    links = soup.find_all('a')

    if len(links) > 1:
        selected_link = links[1]
        href = selected_link.get('href')

        if href:
            return ('https://supremecourt.gov.np/lic/' + href)
        
        
def parse_second_table(url):
    response = rq.post(url)
    soup = bs(response.text , 'lxml')
    table = soup.find_all('table', class_='table-bordered table-striped table-hover')
    data = []

    if len(table)>1:
        details = table[3]

    rows = details.find_all('tr')
    # print(rows)

    for row in rows:
        cols = row.find_all('td')
        # print(cols)
        cols = [ele.text.strip() for ele in cols]
    
        if cols:
            
            data.append(cols)
    
    return data

regno = input('Enter RegNo. : ')
case_details = fetch_case_details(regno)

if case_details:
    data = parse_case_details(case_details)
    second_url = parse_second_url(case_details)
   
    if data:
        df = pd.DataFrame(data)
        df.to_json('table1.json', orient='records', lines=True, indent=4)
    else:
        print('No data is found.') 
    
    if second_url:
        # print(second_url)  
        table = parse_second_table(second_url)
        
        if table:
            # print(table)
            df = pd.DataFrame(table)
            df.to_json('table2.json', orient='records', indent=4)
        else:
            print('No Data') 

    else:
        print('Current State Unavailable')

else:
    print("Case details are empty")



with open('table1.json', 'r') as f:
    data = json.load(f)

# print("Data loaded from JSON:", json.dumps(data, indent=4))

selected_data = {
    'Case Number': data.get('1'),
    'Case Name': data.get('3'),
    'Case status': data.get('4')
}

with open('final.json', 'w') as f:
    json.dump(selected_data, f, indent=4)

# print("Selected details have been written to final.json")



