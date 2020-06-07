import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import re

baseUrl = 'http://www.onefivenine.com/india/pincode/'
zip_code_addr_list = []


def zip_by_address(url, pincode, distrcit, state):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    village_name = soup.find_all("table", width="100%")
    # print(village_name)
    for village in village_name[2:4]:
        for row in village.find_all("tr"):
            columns = row.find_all("td")
            for column in columns:
                addr = re.sub(' +', ' ', column.get_text().replace('\r\n','').strip()).split(',')
                addr.insert(0, pincode)
                if 2 < len(addr) <= 3:
                    addr.append(distrcit)
                    addr.append(state)
                    zip_code_addr_list.append(addr)
                elif len(addr) > 3:
                    zip_code_addr_list.append(addr)


with open("Pincode.csv", newline='', encoding='utf-8') as f:
    count = 0
    try:
        reader_row = csv.reader(f, delimiter=',')
        next(reader_row)
        for row in reader_row:
            zip_by_address(baseUrl + row[4], row[4], row[7], row[8])
        df = pd.DataFrame(zip_code_addr_list, columns=['Pincode', 'Address_line_1', 'Address_Line_2', 'DistrictName','StateName'])
        df_test = pd.read_csv("sample1.csv",delimiter=',', engine='python')
        df_test.columns=['Address_line_1','Address_Line_2','Pincode','taulk','DistrictName','StateName']
        df_test = df_test[['Pincode','Address_line_1','Address_Line_2','taulk','DistrictName','StateName']]
        df_test.drop_duplicates()
        df.drop_duplicates()
        total_addr_df = pd.concat([df,df_test])
        total_addr_df.to_csv('total.csv', encoding='utf-8', index=False, sep=',')

    except Exception as e:
        print(e)
