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
                               ascending=[False,False]).reset_index(drop=True)[:20]



pd.melt(df_scores[['championName','AllyHelp_Score','AllyUseless_Score','utility']].sort_values(['utility','AllyHelp_Score'],ascending=[False,False])[:10],id_vars='championName',var_name='type_score',value_name='score')

#st.dataframe(data = df_visual)

#markdow cabecera (cambiar mas adelante si es posible)

st.markdown(''' 
Definiciones

* AllyHelpScore: Mide que tanto aporta un campeon aliado si te toca en tu equipo.
* AllyUselessScore: Mide que tan inefectivo es un campeon aliado si te toca en tu equipo.
* Utility: Es la resta entre AllyHelpScore y AllyUselessScore, mientras mas grande sea la resta mas util es un campeon y viceversa.

Formulas

frec: Frequence of Appear

AllyHelpScore''')

#grafico
col1, col2 = st.columns(2,gap="large")


with col1:
    st.header("Gráfico de scores")
    st.bar_chart(
        df_visual.set_index('championName'), 
        y=["score"], 
        color="type_score",
        stack=False,
        use_container_width=True  # Ajusta al ancho del contenedor
    )

with col2:
    st.header("Gráfico de utilidad")
    st.bar_chart(
        df_visual.set_index('championName'), 
        y=["utility"],
        color=["#FF8E8E"],
        horizontal=True,
        use_container_width=True  # Ajusta al ancho del contenedor
    )

#tabla
st.header("Tabla de scores")
st.dataframe(data = df_scores,use_container_width=True)

#markdown explicacion


st.latex(r"AllyHelpScore = WinRate(AllyChamp)\times frec(AllyChamp)")
st.latex(r"AllyHelpScore = \frac{wins(AllyChamp)}{frec(AllyChamp)}\times\frac{frec(AllyChamp)}{TotalMatches}")

st.markdown("AllyUselessScore ")

st.latex(r"AllyUselessScore = LoseRate(AllyChamp)\times frec(AllyChamp)")
st.latex(r"AllyUselessScore = \frac{losses(AllyChamp)}{frec(AllyChamp)}\times\frac{frec(AllyChamp)}{TotalMatches}")

st.markdown("Utility")
st.latex(r"Utility = AllyHelpScore - AllyUselessScore")

st.markdown("Los siguientes gráficos muestran los AllyHelpScore, AllyUselessScore y Utility de un jugador seleccionado al azar. Si dicho jugador le tocara un campeon con alta utilidad, puede ser aconsejable que trate de hacer sinergia con dicho aliado. Sin embargo si le toca un campeon con pesima utilidad, puede decidir o bien banearlo o bien dodgear la partida.")







