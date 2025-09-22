import streamlit as st
import pandas as pd
from io import StringIO
import requests


st.title('Streamlit LoL DataProyect')

def load_data(path:str):
    data = pd.read_csv(path,sep=";")
    return data

url = "https://raw.githubusercontent.com/ike-mercado-huanaque/Random-DataScience/refs/heads/master/Proyecto1_lol/visualizacion/visualizacion.csv"
url_graf_scores = "https://raw.githubusercontent.com/ike-mercado-huanaque/Random-DataScience/refs/heads/master/Proyecto1_lol/visualizacion/df_graf_scores.csv"

response = requests.get(url)
df = load_data(StringIO(response.text))

response = requests.get(url_graf_scores)
df_scores = load_data(StringIO(response.text))

df_visual = pd.melt(df_scores
.sort_values(['utility','AllyHelp_Score'],
ascending=[False,False])[['championName','AllyHelp_Score','AllyUseless_Score']],
        id_vars='championName',
        var_name='type_score',
        value_name='score')

st.dataframe(data = df_scores)

st.bar_chart(df_visual,x="championName", y="score", color="type_score")





