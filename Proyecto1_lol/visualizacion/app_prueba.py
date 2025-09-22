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

response2 = requests.get(url_graf_scores)
df_scores = load_data(StringIO(response2.text))

df_visual =  pd.melt(df_scores[['championName','AllyHelp_Score','AllyUseless_Score']],
                     id_vars='championName',
                     var_name='type_score',
                     value_name='score').merge(
                           df_scores[["championName","utility"]],
                           on="championName",
                           how="left").sort_values(
                               ["utility","championName"],
                               ascending=[False,False]).reset_index(drop=True)[:30]



pd.melt(df_scores[['championName','AllyHelp_Score','AllyUseless_Score','utility']].sort_values(['utility','AllyHelp_Score'],ascending=[False,False])[:10],id_vars='championName',var_name='type_score',value_name='score')

#st.dataframe(data = df_visual)

#grafico

col1, col2 = st.columns([2,2])

with col1:
    st.header("Grafico de scores")
    st.bar_chart(df_visual.set_index('championName'), y=["score"], color="type_score",stack=False)
with col2:
    st.header("Grafico de utilidad")
    st.bar_chart(df_visual.set_index('championName'), y=["utility"],color=["#FF8E8E"],horizontal=True)

#tabla
st.header("Tabla de scores")
st.dataframe(data = df_scores)







