from typing import NewType
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementNotVisibleException
import time
import sched
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
# from user_agent_rs import generate_user_agent
import os, gc
# from html.parser import HTMLParser
import re
# from user_agent2 import (
#     generate_user_agent,
# )
from user_agent import generate_user_agent
import pandas as pd
from openpyxl import Workbook

load_dotenv()


chrome_options = Options()

chrome_options.add_argument(f'user-agent={generate_user_agent}')


#estos option ponen lento el web driver
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--disable-webgl")
#---------------------------------------------------------------------------------------

chrome_options.add_argument("no-default-browser-check")

#desactiva los dns
chrome_options.add_argument('--dns-prefetch-disable')

#desactiva las extensiones
chrome_options.add_argument("--disable-extensions")
#desactiva los plugin
chrome_options.add_argument ("-disable-plugins")

#desactiva los anuncios
chrome_options.add_argument ("-disable-popup-block")

chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

chrome_options.add_argument('enable-automation')

#ignora los certificados de seguridad y certificado
chrome_options.add_argument('--ignore-certificate-error')

#ignora los certificados que sean erroneos
chrome_options.add_argument('--ignore-certificate-errors-spki-list')

#desactiva los errores que pueda dar  el ssl
chrome_options.add_argument('--ignore-ssl-errors')

#ejecuta el web scraping en segundo plano
# chrome_options.add_argument('--headless')

# caps = chrome_options.to_capabilities()
desired_capabilities = webdriver.DesiredCapabilities.CHROME
desired_capabilities['acceptInsecureCerts'] = True
desired_capabilities['acceptSslCerts'] = True

PATH = os.getenv('W_PATH')

Ruta_Assets = os.getenv('Ruta_Assets')

Pagina = os.getenv('URL')

URL_Main = os.getenv('URL_MODIFICADA')

s = Service(PATH)

datos = []

def Loteria_Nacional(website = Pagina):

    # datos = []

    try:
        with  webdriver.Chrome(service = s, options=chrome_options, desired_capabilities = desired_capabilities) as driver:

            executor_url = driver.command_executor._url
            session_id = driver.session_id

            driver.get(website)

            """ print(session_id)
            print (executor_url) """

            main(driver, datos)
            # paginacion(driver, datos)
            return datos

            # driver.quit()
            # return datos

    except Exception as e:

        print(e)

    return datos



def main(driver, datos):

    executor_url = driver.command_executor._url
    session_id = driver.session_id

    contenedor = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/section[2]')

    loteria = contenedor.find_elements(By.CLASS_NAME, 'game-block.past')

    for i in loteria:

        # print(i.text)

        titulo = i.text

        titulo_Final = titulo[12:20]

        uno = titulo[11:13]
        dos = titulo[14:16]
        tres = titulo[17:19]

        fechafinal = titulo[0:10]

        dic = dict( fecha = fechafinal, Primer_Numero = uno, Segundo_Numero = dos, Tercer_Numero = tres)

        datos.append(dic)
    print(datos)
    return datos



# Loteria_Nacional()

try:

    for i in range(2017, 2022):

        for e in range(10, 31, 10):
        # loto += 10
        # if loto % 10 == 0:
        #     continue
        
        
            website = f'{URL_Main}'

            P_Loteria = Loteria_Nacional(website)
            if i == Exception:
                print(i)
                break
except Exception as e:
    print(e, "Linea 152")


pedro = pd.DataFrame(datos)



pedro.to_excel(Ruta_Assets, sheet_name='WebScraping')

# pedro = pd.DataFrame(periodico, columns=['Periodico'])


#si quito el parametro de la columna me imprime los datos en una sola fila
#antes me daba un error porque no estaba encasulando los datos de firebasse en un arreglo

# Ruta_excel = os.getenv('Ruta')

