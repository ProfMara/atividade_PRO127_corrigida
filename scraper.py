from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver
import os

# PROCURE A VERSÃO DO SEU CHROME ASSIM:
# Clique nos 3 pontinhos -> Configurações -> Sobre o Chrome -> veja a versão

# LINK PARA ACHAR O WEBDRIVER NA VERSÃO CERTA
# https://googlechromelabs.github.io/chrome-for-testing/#stable

# SELECIONE A URL DA VERSAO DO WEBDRIVER DO SEU CHROME, COPIE E COLE NO NAVEGADOR
# FAÇA O DOWNLOAD, EXTRAIA A PASTA NESTA PASTA

# Se trocar o ChromeDriver, atualize o endereço abaixo
# para o endereço do seu chromedriver do seu PC
dir = os.getcwd() + '\chromedriver-win64\chromedriver.exe'

#acessando o chrome driver no endereço guardado na variável dir
service = webdriver.ChromeService(executable_path=dir)

driver = webdriver.Chrome(service=service)

# URL dos Exoplanetas da NASA
driver.get('https://exoplanets.nasa.gov/exoplanet-catalog/')

time.sleep(10)

planets_data = []


def scrape():

    for i in range(0, 10):
        print(f'Coletando dados da página {i+1} ...')

        # Objeto BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Loop para encontrar o elemento dentro das tags ul e li
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):

            li_tags = ul_tag.find_all("li")

            temp_list = []

            for index, li_tag in enumerate(li_tags):

                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")

            planets_data.append(temp_list)

        # Encontre o botão na página e clique para passar para a próxima página
        driver.find_element(
            by=By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()


# Chamando o método
scrape()

# Defina o cabeçalho
headers = ["name", "light_years_from_earth",
           "planet_mass", "stellar_magnitude", "discovery_date"]

# Defina o dataframe do pandas
dataframe = pd.DataFrame(planets_data, columns=headers)

# Converta para CSV
dataframe.to_csv('scraped_data.csv', index=True, index_label="id")
