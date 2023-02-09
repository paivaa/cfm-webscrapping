pip install -U selenium
pip install webdriver_manager

import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

arquivo = "<ARQUIVO>.xlsx"

url = "https://portal.cfm.org.br/busca-medicos/"

df = pd.read_excel(arquivo)

ser = Service(ChromeDriverManager().install())
op = webdriver.ChromeOptions()
op.add_argument("--incognito")


lista = []


for index, row in df.iterrows():
    print("Index: "+str(index)+ " e o nome do medico é "+row["NOME"])
    chrome = webdriver.Chrome(service=ser, options=op)
    chrome.get(url)
    
    time.sleep(5)
    
    elemento_nome_medico = chrome.find_element(By.XPATH, '//*[@id="buscaForm"]/div/div[1]/div[1]/div/input')
    elemento_numero_crm = chrome.find_element(By.XPATH, '//*[@id="buscaForm"]/div/div[1]/div[3]/div/input')
    elemento_botao_buscar = chrome.find_element(By.XPATH, '//*[@id="buscaForm"]/div/div[4]/div[2]/button')
    elemento_botao_aceito = chrome.find_element(By.XPATH, '//*[@id="page"]/div[4]/div[2]/button')
    
    elemento_botao_aceito.click()
    elemento_nome_medico.send_keys(row["NOME"]) 
    elemento_numero_crm.send_keys(row["CRM"])
    elemento_botao_buscar.click()
    
    time.sleep(7)
    
    elemento_especialidade = chrome.find_elements(By.XPATH, '//*[@id="content"]/section[2]/div/div/div/div[1]/div/div/div/div[2]/div/div[5]/div')
    
    if len(elemento_especialidade) > 0 and elemento_especialidade[0].is_displayed():
        if elemento_especialidade[0].text == "Endereço: Exibição não autorizada pelo médico.":
            item = {
                'NOME': row["NOME"],
                'FOUND_CFM': 'TRUE',
                'ESPECIALIDADE': 'GENERALISTA',
            }
            print(item)
            lista.append(item)
        else:
            item = {
                'NOME': row["NOME"],
                'FOUND_CFM': 'TRUE',
                'ESPECIALIDADE': elemento_especialidade[0].text,
            }
            print(item)
            lista.append(item)
    else:
        item = {
                'NOME': row["NOME"],
                'FOUND_CFM': 'FALSE',
                'ESPECIALIDADE': '',
            }
        print(item)
        lista.append(item)
        
    chrome.close()

df_gerado = pd.DataFrame(lista)
df_gerado.to_excel('lista.xlsx', index=False)
print('FIM')

