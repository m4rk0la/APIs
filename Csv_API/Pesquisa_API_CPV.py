import pandas as pd
import requests
import json
import os

data = {
    "grant_type": "",
    "client_id": "",
    "client_secret": "",
    "username": "######",
    "password": "######",
    "scope": ""
}
chamado = requests.post("########", data=data)
chamado.raise_for_status()
print(chamado.status_code)

tok = chamado.json()["access_token"]
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
    "Authorization": f"Bearer {tok}"
}

testtoken = requests.post("########", headers=headers)
testtoken.raise_for_status()
print(testtoken.content)
headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer ' + tok
}
params = {
    'cpv__is': '33690000',
    # 'buyer_name__is' : 'CENTRAL DE ABASTECIMIENTO DEL SISTEMA NACIONAL DE SERVICIO DE SALUD, Compras del Giro 621',
    'buyer_address_country_name__is': 'Chile',
    # 'buyer_address_country_code__is': 'HK',
    'release_date__gte': '2023-05-01T00:00:00',
    # 'tender_deadline__gte' : '2023-05-31T00:00:00',
    'compiled_only': 'false',
    'original_only': 'false',
    'date_direction': 'desc',
    'offset': '0',
    'limit': '100'
}
chamado = requests.post("########", data=data)
chamado.raise_for_status()
print(chamado.status_code)
print(chamado.content)

tok = chamado.json()["access_token"]

chamado = requests.get('########', headers=headers,
                       params=params)
print(chamado.status_code)
resposta_JSON = json.loads(chamado.content)

df = pd.DataFrame(resposta_JSON)

name_list = []
endDate_list = []
startDate_list = []
descr_list = []
title_list = []
language_list = []
link_list = []
cpv_list = []

for i in range(101):  
    if i < len(df['results']):
        
        try:
            name = df['results'][i]['releases'][0]['parties'][0]['name']
        except KeyError:
            name = 'X'
        name_list.append(name)
        
        try:
            endDate = df['results'][i]['releases'][0]['tender']['tenderPeriod']['endDate']
        except KeyError:
            endDate = 'X'
        endDate_list.append(endDate)
        
        try:
            startDate = df['results'][i]['releases'][0]['tender']['tenderPeriod']['startDate']
        except KeyError:
            startDate = 'x'
        startDate_list.append(startDate)
        
        try:
            descr = df['results'][i]['releases'][0]['tender']['description']
        except KeyError:
            descr = 'X'
        descr_list.append(descr)
        
        try:
            title = df['results'][i]['releases'][0]['tender']['title']
        except KeyError:
            title = 'X'
        title_list.append(title)
        
        try:
            language = df['results'][0]['releases'][0]['language']
        except KeyError:
            language = 'X'
        language_list.append(language)
        
        try:
            link = df['results'][i]['releases'][0]['tender']['documents'][0]['url']
        except KeyError:
            link = 'X'
        link_list.append(link)
        
        try:
            cpv = df['results'][0]['releases'][1]['tender']['items'][0]['additionalClassifications'][0]['id']
        except KeyError:
            cpv = 'X'
        cpv_list.append(cpv)
        
    else:
        break 
    
data = {'name': name_list,
        'title' : title_list,
        'description' : descr_list,
        'cpv' : cpv_list,
        'StartDate':startDate_list,
        'EndDate' : endDate_list,
        'link':link_list,
        'language':language_list}

df_new = pd.DataFrame(data)
desktop_path = os.path.expanduser("~/Desktop")
excel_file_path = os.path.join(desktop_path, "resultadosTESTE.xlsx")
df_new.to_excel(excel_file_path, index=False)