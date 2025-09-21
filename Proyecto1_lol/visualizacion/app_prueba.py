import streamlit as st
import pandas as pd

df = pd.read_csv("visualizacion.csv", sep=";")

st.title('My app :)')
st.dataframe(df)

st.line_chart(df['championId'])
st.bar_chart(df['championId'])


