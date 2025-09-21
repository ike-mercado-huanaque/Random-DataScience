import streamlit as st
import pandas as pd
from io import StringIO
import requests


st.title('Streamlit LoL DataProyect')

def load_data(path:str):
    data = pd.read_csv(path,sep=";")
    return data

url = "https://raw.githubusercontent.com/ike-mercado-huanaque/Random-DataScience/refs/heads/master/Proyecto1_lol/visualizacion/visualizacion.csv"
response = requests.get(url)
df = load_data(StringIO(response.text))
st.write(df)





