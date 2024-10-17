import pandas as pd
from tinydb import TinyDB


colecao_partidas1 = TinyDB("db/base_flashscore_temp_atual.json")
df = pd.DataFrame(colecao_partidas1.all())


df = df.sort_values(["Date", "Time"])

df = df.dropna()
df = df.reset_index(drop=True)
df.index += 1


df.to_csv('base_excel/base_flashscore.csv',index=False)