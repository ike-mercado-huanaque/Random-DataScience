import streamlit as st
import pymysql
import pandas as pd

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    database='database_name'
)

sql_query = "SELECT \nidpartida,puuid,championId,championName,win\nFROM \npartidas\nWHERE\nidpartida IN (SELECT idpartida \nFROM partidas \nWHERE TRIM(riotIdGameName) = TRIM('EDUPOIO')\n)"
df = pd.read_sql(sql_query, conn)

st.title('My app :)')
st.dataframe(df)

st.line_chart(df['championId'])
st.bar_chart(df['championId'])


conn.close()
