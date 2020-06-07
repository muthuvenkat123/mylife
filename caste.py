import requests
import string
import pandas as pd

url = 'http://www.ncbc.nic.in/SearchService.asmx/GetCompanyInfo'
obc_caste_list = []

def obc_caste(search_name):
    data = {"prefixText": search_name, "count": 10, "contextKey": "WORKS_CAST,CastEnglish,CastEnglish"}
    res = requests.post(url, json=data)
    for val in res.json().values():
        if len(val):
            print(val)
            obc_caste_list.append(val)

if __name__ == '__main__':
    # for search_name in range(0, 10):
    #     obc_caste(search_name)
    obc_caste('C')
    for search_name in string.ascii_uppercase:
        obc_caste(search_name)

    obc_caste('C')
    df = pd.DataFrame(obc_caste_list)
    df.to_csv('caste.csv', encoding='utf-8')
