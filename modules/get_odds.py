from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import  NoSuchElementException
import re
from time import sleep
class GetOdds:
    def __init__(self, driver):
        self.driver = driver

    def get_match_details(self, id_jogo, jogo, season):
        """Método para obter detalhes gerais do jogo."""
        jogo['Season'] = season
        self.driver.get(f'https://www.flashscore.com.br/jogo/{id_jogo}/#/resumo-de-jogo/resumo-de-jogo')
        jogo['Id'] = id_jogo

        # País
        country = self.driver.find_element(By.CSS_SELECTOR, 'span.tournamentHeader__country').text.split(':')[0]

        # Data e Hora
        date = self.driver.find_element(By.CSS_SELECTOR, 'div.duelParticipant__startTime').text.split(' ')[0]
        jogo['Date'] = date.replace('.', '/')
        time = self.driver.find_element(By.CSS_SELECTOR, 'div.duelParticipant__startTime').text.split(' ')[1]
        jogo['Time'] = time

        # Liga
        league = self.driver.find_element(By.CSS_SELECTOR, 'span.tournamentHeader__country > a').text.split(' -')[0]
        jogo['League'] = f'{country} - {league}'

        # Home e Away
        home = self.driver.find_element(By.CSS_SELECTOR, 'div.duelParticipant__home').find_element(By.CSS_SELECTOR, 'div.participant__participantName').text
        jogo['Home'] = home
        away = self.driver.find_element(By.CSS_SELECTOR, 'div.duelParticipant__away').find_element(By.CSS_SELECTOR, 'div.participant__participantName').text
        jogo['Away'] = away

        # Rodada
        try:
            rodada = self.driver.find_element(By.CSS_SELECTOR, 'span.tournamentHeader__country > a').text.split('- ')[1]
            jogo['Round_number'] = rodada
        except IndexError:
            jogo['Round_number'] = '-'
        except NoSuchElementException:
            jogo['Round_number'] = '-'
            
    def get_match_details_historic(self, id_jogo, jogo, season):
        """Método para obter detalhes historicos gerais do jogo."""
        jogo['Season'] = season
        self.driver.get(f'https://www.flashscore.com.br/jogo/{id_jogo}/#/resumo-de-jogo/resumo-de-jogo')
        jogo['Id'] = id_jogo

        # País
        country = self.driver.find_element(By.CSS_SELECTOR, 'span.tournamentHeader__country').text.split(':')[0]

        # Data e Hora
        date = self.driver.find_element(By.CSS_SELECTOR, 'div.duelParticipant__startTime').text.split(' ')[0]
        jogo['Date'] = date.replace('.', '/')
        time = self.driver.find_element(By.CSS_SELECTOR, 'div.duelParticipant__startTime').text.split(' ')[1]
        jogo['Time'] = time

        # Liga
        league = self.driver.find_element(By.CSS_SELECTOR, 'span.tournamentHeader__country > a').text.split(' -')[0]
        jogo['League'] = f'{country} - {league}'

        # Home e Away
        home = self.driver.find_element(By.CSS_SELECTOR, 'div.duelParticipant__home').find_element(By.CSS_SELECTOR, 'div.participant__participantName').text
        jogo['Home'] = home
        away = self.driver.find_element(By.CSS_SELECTOR, 'div.duelParticipant__away').find_element(By.CSS_SELECTOR, 'div.participant__participantName').text
        jogo['Away'] = away

        # Rodada
        try:
            rodada = self.driver.find_element(By.CSS_SELECTOR, 'span.tournamentHeader__country > a').text.split('- ')[1]
            jogo['Round_number'] = rodada
        except IndexError:
            jogo['Round_number'] = '-'
        except NoSuchElementException:
            jogo['Round_number'] = '-'

        # Placar e Gols FT
        placar = self.driver.find_elements(By.CSS_SELECTOR, 'div.duelParticipant__score')[0].text
        jogo['placar'] = placar
        numeros = re.findall(r'\d+', placar)
        placar_1 = numeros[0]
        placar_2 = numeros[1]
        jogo['FT_Goals_H'] = placar_1
        jogo['FT_Goals_A'] = placar_2

        del jogo['placar']
                                   
            
    def get_odds_1x2(self, id_jogo, jogo):
        """Método para obter odds de 1x2 do jogo no Tempo Regulamentar."""
        url_ml_full_time = f'https://www.flashscore.com.br/jogo/{id_jogo}/#/comparacao-de-odds/1x2-odds/tempo-regulamentar'
        self.driver.get(url_ml_full_time)
        WebDriverWait(self.driver, 8).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.ui-table')))
        table_odds = self.driver.find_element(By.CSS_SELECTOR, 'div.ui-table')
        linha_ml_ft = table_odds.find_element(By.CSS_SELECTOR, 'div.ui-table__row')
        jogo['FT_Odd_ML_Bookie'] = linha_ml_ft.find_element(By.CSS_SELECTOR, 'img.prematchLogo').get_attribute('title')
        jogo['FT_Odd_ML_H'] = float(linha_ml_ft.find_elements(By.CSS_SELECTOR, 'a.oddsCell__odd')[0].text)
        jogo['FT_Odd_ML_D'] = float(linha_ml_ft.find_elements(By.CSS_SELECTOR, 'a.oddsCell__odd')[1].text)
        jogo['FT_Odd_ML_A'] = float(linha_ml_ft.find_elements(By.CSS_SELECTOR, 'a.oddsCell__odd')[2].text)  
        
        
    def get_ou_first_half(self, id_jogo, jogo):
        """Obtém odds de Acima/Abaixo do 1º Tempo."""
        url_ou_first_half = f'https://www.flashscore.com.br/jogo/{id_jogo}/#/comparacao-de-odds/acima-abaixo/1-tempo'
        self.driver.get(url_ou_first_half)
        sleep(1)
        
        if self.driver.current_url == url_ou_first_half:
            WebDriverWait(self.driver, 8).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.ui-table')))
            linhas = self.driver.find_elements(By.CSS_SELECTOR, 'div.ui-table__body')

            for linha in linhas:
                if len(linha.find_elements(By.CSS_SELECTOR, 'a.oddsCell__odd')) > 1:
                    bookie = linha.find_element(By.CSS_SELECTOR, 'img.prematchLogo').get_attribute('title')
                    total_gols = linha.find_element(By.CSS_SELECTOR, 'span.oddsCell__noOddsCell').text.replace('.', '')

                    if total_gols == '05':
                        over = float(linha.find_elements(By.CSS_SELECTOR, 'a.oddsCell__odd')[0].text)
                        under = float(linha.find_elements(By.CSS_SELECTOR, 'a.oddsCell__odd')[1].text)
                        jogo[f'HT_Odd_OU_{total_gols}_Bookie'] = bookie
                        jogo[f'HT_Odd_Over{total_gols}'] = over
                        jogo[f'HT_Odd_Under{total_gols}'] = under
                        

    def get_ou_full_time(self, id_jogo, jogo):
        """Obtém odds de Acima/Abaixo do Tempo Regulamentar."""
        url_ou_full_time = f'https://www.flashscore.com.br/jogo/{id_jogo}/#/comparacao-de-odds/acima-abaixo/tempo-regulamentar'
        self.driver.get(url_ou_full_time)
        sleep(1)
        
        if self.driver.current_url == url_ou_full_time:
            WebDriverWait(self.driver, 8).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.ui-table')))
            linhas = self.driver.find_elements(By.CSS_SELECTOR, 'div.ui-table__body')

            for linha in linhas:
                if len(linha.find_elements(By.CSS_SELECTOR, 'a.oddsCell__odd')) > 1:
                    bookie = linha.find_element(By.CSS_SELECTOR, 'img.prematchLogo').get_attribute('title')
                    total_gols = linha.find_element(By.CSS_SELECTOR, 'span.oddsCell__noOddsCell').text.replace('.', '')

                    if total_gols in ['05', '15', '25', '35', '45']:
                        over = float(linha.find_elements(By.CSS_SELECTOR, 'a.oddsCell__odd')[0].text)
                        under = float(linha.find_elements(By.CSS_SELECTOR, 'a.oddsCell__odd')[1].text)
                        jogo[f'FT_Odd_OU_{total_gols}_Bookie'] = bookie
                        jogo[f'FT_Odd_Over{total_gols}'] = over
                        jogo[f'FT_Odd_Under{total_gols}'] = under

    def get_btts_full_time(self, id_jogo, jogo):
        """Obtém odds de Ambos Marcam (BTTS) no Tempo Regulamentar."""
        url_btts_full_time = f'https://www.flashscore.com.br/jogo/{id_jogo}/#/comparacao-de-odds/ambos-marcam/tempo-regulamentar'
        self.driver.get(url_btts_full_time)
        sleep(1)

        if self.driver.current_url == url_btts_full_time:
            WebDriverWait(self.driver, 8).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.ui-table')))
            linha = self.driver.find_element(By.CSS_SELECTOR, 'div.ui-table__row')

            bookie_btts = linha.find_element(By.CSS_SELECTOR, 'img.prematchLogo').get_attribute('title')
            jogo['FT_Odd_BTTS_Bookie'] = bookie_btts
            jogo['FT_Odd_BTTS_Yes'] = float(linha.find_elements(By.CSS_SELECTOR, 'a.oddsCell__odd')[0].text)
            jogo['FT_Odd_BTTS_No'] = float(linha.find_elements(By.CSS_SELECTOR, 'a.oddsCell__odd')[1].text)        

