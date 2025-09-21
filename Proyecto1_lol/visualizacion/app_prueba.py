import streamlit as st
import pandas as pd



st.title('Streamlit LoL DataProyect')

def load_data(path:str):
    data = pd.read_csv(path,sep=";")
    return data

df = load_data("./visualizacion.csv")
st.write(df)





