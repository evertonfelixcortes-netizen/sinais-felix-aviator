import streamlit as st
import numpy as np
import requests
from bs4 import BeautifulSoup
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Sinais do Felix-Aviator", layout="centered")

st.title("🚀 Sinais do Felix-Aviator")

@st.cache_data(ttl=60)
def obter_dados():
    url = "https://www.tipminer.com/br/historico/sortenabet/aviator"
    try:
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        spans = soup.find_all("span")

        valores = []
        for s in spans:
            txt = s.text.replace("x","").strip()
            try:
                v = float(txt)
                if 1 <= v <= 100:
                    valores.append(v)
            except:
                pass

        return valores[:200]
    except:
        return []

def treinar(dados):
    X, y = [], []
    for i in range(10, len(dados)):
        X.append(dados[i-10:i])
        if dados[i] >= 10:
            y.append(2)
        elif dados[i] >= 2:
            y.append(1)
        else:
            y.append(0)

    modelo = RandomForestClassifier(n_estimators=150)
    modelo.fit(X, y)
    return modelo

dados = obter_dados()

if not dados:
    st.error("Erro ao carregar dados")
    st.stop()

modelo = treinar(dados)
ultimos = dados[:10]

if st.button("🔮 GERAR SINAL"):
    pred = modelo.predict([ultimos])[0]

    if pred == 2:
        st.error("🔥 Buscar 10x")
    elif pred == 1:
        st.success("🟢 Buscar 2x–5x")
    else:
        st.warning("🔴 Evitar")

st.write("Últimos resultados:")
st.write(dados[:20])
