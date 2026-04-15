import streamlit as st
import numpy as np
import requests
from bs4 import BeautifulSoup
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Sinais do Felix-Aviator", layout="centered")

st.title("🚀 Sinais do Felix-Aviator")

# =============================
# PEGAR DADOS
# =============================
@st.cache_data(ttl=60)
def obter_dados():
    url = "https://www.tipminer.com/br/historico/sortenabet/aviator"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text

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

# =============================
# TREINAR IA
# =============================
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

    modelo = RandomForestClassifier(n_estimators=100)
    modelo.fit(X, y)
    return modelo

# =============================
# EXECUÇÃO
# =============================
dados = obter_dados()

if not dados:
    st.warning("⚠️ Não conseguiu pegar dados do site")
    dados = [1.2, 1.5, 2.0, 1.1, 3.2, 1.3, 2.5, 1.8, 1.4, 2.2, 1.7, 2.8]

modelo = treinar(dados)

ultimos = dados[:10]

# =============================
# BOTÃO
# =============================
if st.button("🔮 GERAR SINAL"):
    pred = modelo.predict([ultimos])[0]

    if pred == 2:
        st.error("🔥 Buscar 10x")
    elif pred == 1:
        st.success("🟢 Buscar 2x–5x")
    else:
        st.warning("🔴 Evitar")

# =============================
# INFO
# =============================
st.write("📊 Últimos resultados:")
st.write(dados[:20])
