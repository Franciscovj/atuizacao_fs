from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm.auto import tqdm
import pandas as pd
import os
import warnings
from modules.Ligas import ligas
from modules.get_odds import GetOdds

warnings.filterwarnings("ignore")

# Configurações do Firefox
firefox_options = Options()
#firefox_options.add_argument("--headless")  # Executa em modo headless

# Inicia o serviço do GeckoDriver
service = Service('geckodriver.exe')  

# Cria uma instância do Firefox
driver = webdriver.Firefox(service=service, options=firefox_options)

data = GetOdds(driver)
driver.maximize_window()


df = pd.DataFrame()
for liga in tqdm(ligas):
    url = f'https://www.flashscore.com.br/futebol/{liga}/calendario/'
    driver.get(url)

    try:
        WebDriverWait(driver, 8).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'button#onetrust-accept-btn-handler')))
        button_cookies = driver.find_element(By.CSS_SELECTOR,'button#onetrust-accept-btn-handler')
        button_cookies.click()
    except:
        print("cookies already closed")
        
    sleep(3)    
        
    jogos = driver.find_elements(By.CSS_SELECTOR,'div.event__match')

    sleep(3)
    jogos_data = []
    id_jogos =[]

    for i in jogos:
        id_jogos.append(i.get_attribute("id")[4:])  
        id_jogos = id_jogos[:2] 
        
    season = driver.find_element(By.CSS_SELECTOR,'div.heading__info').text 
    print(driver.title)

    for id_jogo in tqdm(id_jogos):

        try:
            jogo = {}

            # Obter detalhes gerais do jogo
            data.get_match_details(id_jogo=id_jogo , jogo=jogo, season=season)

            # Obter odds de 1x2 do jogo no Tempo Regulamentar
            data.get_odds_1x2(id_jogo=id_jogo , jogo=jogo)
                        
            # Obter odds de Acima/Abaixo do 1º Tempo
            data.get_ou_first_half(id_jogo=id_jogo , jogo=jogo)

            # Obter odds de Acima/Abaixo do Tempo Regulamentar
            data.get_ou_full_time(id_jogo=id_jogo , jogo=jogo)

            # Obter odds de Ambos Marcam (BTTS) no Tempo Regulamentar
            data.get_btts_full_time(id_jogo=id_jogo , jogo=jogo)
           
            jogos_data.append(jogo)               
            df_liga = pd.DataFrame(jogos_data)
            df = pd.concat([df, df_liga], ignore_index=True)
            df.sort_values(['Date','Time'], inplace=True)
            df.reset_index(drop=True, inplace=True)
            df.index = df.index + 1
            df.index.name = 'Nº'
            #print(jogo)                
                                
                
        except:
            print(f'Erro ao coletar dados do jogo {id_jogo}')
            sleep(0.5) 
            
 
driver.quit()             
df = df[
    [
        "Id",
        "Date",
        "Time",
        "League",
        "Season",
        "Round_number",
        "Home",
        "Away",
        "FT_Odd_ML_H",
        "FT_Odd_ML_D",
        "FT_Odd_ML_A",
        "HT_Odd_Over05",
        "HT_Odd_Under05",
        "FT_Odd_Over05",
        "FT_Odd_Under05",
        "FT_Odd_Over15",
        "FT_Odd_Under15",
        "FT_Odd_Over25",
        "FT_Odd_Under25",
        "FT_Odd_Over35",
        "FT_Odd_Under35",
        "FT_Odd_Over45",
        "FT_Odd_Under45",
        "FT_Odd_BTTS_Yes",
        "FT_Odd_BTTS_No",
    ]
]

df.columns = [
    "Id",
    "Date",
    "Time",
    "League",
    "Season",
    "Round",
    "Home",
    "Away",
    "FT_Odd_H",
    "FT_Odd_D",
    "FT_Odd_A",
    "HT_Odd_Over05",
    "HT_Odd_Under05",
    "FT_Odd_Over05",
    "FT_Odd_Under05",
    "FT_Odd_Over15",
    "FT_Odd_Under15",
    "FT_Odd_Over25",
    "FT_Odd_Under25",
    "FT_Odd_Over35",
    "FT_Odd_Under35",
    "FT_Odd_Over45",
    "FT_Odd_Under45",
    "Odd_BTTS_Yes",
    "Odd_BTTS_No",
]
  
df.drop_duplicates(subset=['Id'], inplace=True)



diretorio ="base_excel"
if not os.path.exists(diretorio):
    os.makedirs(diretorio)
    
df.to_excel(os.path.join(diretorio, 'jogos_do_dia.xlsx'), index=False)       
                 