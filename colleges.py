import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import re
import PyPDF2
import tabula



deemedUrl = ['https://www.ugc.ac.in/deemeduniversity.aspx', 'https://www.ugc.ac.in/stateuniversity.aspx',
             'https://www.ugc.ac.in/centraluniversity.aspx']
universityUrl = 'https://www.ugc.ac.in/'
private_url = 'https://www.ugc.ac.in/print_privateuniversity.aspx'
deemed_india_state_list = {}
india_deemed_university = []
collage_list=[]


def deemed_university(url):
    state = requests.get(url)
    soap = BeautifulSoup(state.text, 'html.parser')
    data = soap.find_all("table")
    for reference in data:
        url_ref = reference.find_all("a")
        for url in url_ref:
            deemed_india_state_list[url.get_text().strip()] = universityUrl + url["href"]


def process_deemed_university(deemed_list):
    for keys, value in deemed_list.items():
        state = requests.get(value)
        soap = BeautifulSoup(state.text, 'html.parser')
        for ref in soap.find_all("tr"):
            india_deemed_university.append([keys, ref.find('font').get_text().strip()])


def process_private_university():
    private_data = requests.get(private_url)
    data = BeautifulSoup(private_data.text, 'html.parser')
    soap = data.find_all('table')
    for ref in soap:
        for collage in ref.find_all('table'):
            for record in collage.find_all('tr'):
                for collage_name in record.find_all('td', style="width:34%;"):
                    coll_value = collage_name.get_text().strip()
                for college_state in record.find_all('td', style="width:30%;"):
                    coll_key = college_state.get_text().strip().split(',')[-1].split('-')[0].strip()
                    india_deemed_university.append([coll_key, coll_value])


def autonomous_colleges(cnt):
    pdf = PyPDF2.PdfFileReader("autonomous.pdf", "rb")
    text_data = pdf.getPage(cnt).extractText().strip()
    str = ''.join(text_data.split("\t\r\n"))
    # print(str)
    # print(str)
    # str1="1.  Andhra Loyla College, hello"
    # reg=r'\d+\.\s+.*[,]+'
    # print(re.findall(reg, str1))
    pattern = r"\d+\.\s+[a-zA-Z0-9\s\.&\\™]+"
    result = re.findall(pattern, str)
    for data in result:
        coll = re.sub(' +', ' ', data)
        final_str=(','.join(coll.split('\n'))).replace(',','')
        coll_list=re.findall(r'[a-zA-Z]+.*',final_str)
        for collage_name in coll_list:
            collage_list.append(collage_name)

    # df=tabula.read_pdf("college.pdf", pages='all')
    # print(df)


def college_all(cnt):
    pdf = PyPDF2.PdfFileReader('colleges.pdf', 'rb')
    text_data = pdf.getPage(cnt).extractText().strip()
    pattern = r'2\(f\)\s+.+\s+.+\s*.*\s*.*(?:Institute|Research|Work|Mahavidyaloaya|Mahavidyapith|Mahavidyalaya|Girls|Arts|Law|Economics|Commerce|Management|Culture|Architecture|Transport|School|Institutions|College|Education|Science|Technology|Sciences|Women|Pharmacy|Kalasala|Engineeing|Studies)'
    # re.MULTILINE
    re.I
    result = re.findall(pattern, text_data)
    for data in result:
        coll_name=','.join((data.split('\n'))[1:]).replace(',', '')
        collage_list.append(coll_name)


if __name__ == "__main__":
    for demurl in deemedUrl:
        deemed_university(demurl)
        process_deemed_university(deemed_india_state_list)
    process_private_university()
    df1 = pd.DataFrame(india_deemed_university, columns=['State', 'College_name'])
    del df1['State']
    # df.to_csv('universites.csv', encoding='utf-8', index=False, sep=',')
    for inp in range(56):
        autonomous_colleges(inp + 3)
    for inp in range(1549):
        college_all(inp+1)
    df2=pd.DataFrame(collage_list,columns=['College_name'])
    # df.to_csv('college_list.csv', encoding='utf-8', index=False, sep=',')
    df_final=pd.concat([df1, df2])
    df_final.to_csv('college_list.csv', encoding='utf-8', index=False, sep=',')

