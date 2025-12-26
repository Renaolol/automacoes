from bs4 import BeautifulSoup
import requests
import pandas as pd


site = requests.get('https://www.ibge.gov.br/')
print(site)
soup = BeautifulSoup(site.text,'lxml')
print(soup.find_all('h3'))



