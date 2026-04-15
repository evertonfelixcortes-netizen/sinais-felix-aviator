import streamlit as st
import numpy as np
import requests
from bs4 import BeautifulSoup
from sklearn.ensemble import RandomForestClassifier
import json
import os

st.set_page_config(page_title="Sinais do Felix-Aviator", layout="centered")

st.title("🚀 Sinais do Felix-Aviator")

ARQUIVO = "dados.json"

# =============================
# PEGAR DADOS DO SITE
# =============================
def pegar_site():
    url = "https://www.tipminer.com/br/historico/sortenabet/aviator"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        spans = soup.find_all("span")
        valores = []

        for s in spans:
            txt = s.text.replace("x", "").strip()
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
# SALVAR DADOS
# =============================
def salvar(dados):
    with open(ARQUIVO, "w") as f:
        json.dump(dados, f)

# =============================
# CARREGAR DADOS SALVOS
# =============================
def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    return []

# =============================
# OBTER DADOS (INTELIGENTE)
# =============================
dados = pegar_site()

if dados:
    salvar(dados)
    st.success("✅ Dados atualizados do site")
else:
    dados = carregar()
    st.warning("⚠️ Usando dados salvos (site bloqueou)")

if not dados:
    st.error("❌ Nenhum dado disponível")
    st.stop()

# =============================
# IA
# =============================
def treinar(dados):
    X, y = [], []
    
    for i in range(5, len(dados)):
        X.append(dados[i-5:i])

        if dados[i] >= 10:
            y.append(2)
        elif dados[i] >= 2:
            y.append(1)
        else:
            y.append(0)

    modelo = RandomForestClassifier(n_estimators=100)
    modelo.fit(X, y)
    return modelo

modelo = treinar(dados)

ultimos = dados[:5]

# =============================
# SINAL
# =============================
if st.button("🔮 GERAR SINAL"):
    pred = modelo.predict([ultimos])[0]

    if pred == 2:
        st.error("🔥 Possível 10x (alto risco)")
    elif pred == 1:
        st.success("🟢 Entrar (2x–5x)")
    else:
        st.warning("🔴 Evitar")

# =============================
# INFO
# =============================
st.write("📊 Últimos resultados:")
st.write(dados[:20])
