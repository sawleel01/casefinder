import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
import json

def fetch_case_details(regno):
    url = 'https://supremecourt.gov.np/lic/sys.php?d=reports&f=case_details&num=1&mode=view&caseno=215144'
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


regno = input('Enter RegNo. : ')
case_details = fetch_case_details(regno)

if case_details:
    data = parse_case_details(case_details)
    if data:
        df = pd.DataFrame(data)
        df.to_json('details.json', orient='records', lines=True, indent=4)
    else:
        print('No data is found.')
else:
    print("Case details are empty")


