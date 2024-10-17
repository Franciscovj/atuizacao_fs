from tinydb import TinyDB, Query
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm.auto import tqdm
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



for liga in tqdm(ligas):
    colecao_partidas = TinyDB('db/base_flashscore_temp_atual.json')
    url = f'https://www.flashscore.com.br/futebol/{liga}/resultados/'
    driver.get(url)

    try:
        # Tenta fechar o banner de cookies
        WebDriverWait(driver, 8).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler')))
        button_cookies = driver.find_element(By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler')
        button_cookies.click()
    except:
        print("Cookies banner already closed or not found.")
        

    sleep(3)
    while True:
        botoes_proxima_pagina = driver.find_elements(By.CSS_SELECTOR, 'a.event__more--static')
        if not botoes_proxima_pagina:
            break
        botoes_proxima_pagina[0].click()
        sleep(3) 
        

    jogos = driver.find_elements(By.CSS_SELECTOR,'div.event__match')

    sleep(3)

    id_jogos =[]

    for i in jogos:
        id_jogos.append(i.get_attribute("id")[4:])  
        #id_jogos = id_jogos[:5] 
        
    season = driver.find_element(By.CSS_SELECTOR,'div.heading__info').text 
    print(driver.title)

    for id_jogo in tqdm(id_jogos):
        procura_duplicado = Query()
        if colecao_partidas.search(procura_duplicado.Id == id_jogo) == []:
            try:
                jogo = {}
                # Obter detalhes gerais do jogo
                data.get_match_details_historic(id_jogo=id_jogo , jogo=jogo, season=season)

                # Obter odds de 1x2 do jogo no Tempo Regulamentar
                data.get_odds_1x2(id_jogo=id_jogo , jogo=jogo)
                            
                # Obter odds de Acima/Abaixo do 1º Tempo
                data.get_ou_first_half(id_jogo=id_jogo , jogo=jogo)

                # Obter odds de Acima/Abaixo do Tempo Regulamentar
                data.get_ou_full_time(id_jogo=id_jogo , jogo=jogo)

                # Obter odds de Ambos Marcam (BTTS) no Tempo Regulamentar
                data.get_btts_full_time(id_jogo=id_jogo , jogo=jogo)               
                    
                                    
                colecao_partidas.insert(jogo.copy())
                    
            except:
                print(f'Erro ao coletar dados do jogo {id_jogo}')
                sleep(0.5) 

driver.quit()