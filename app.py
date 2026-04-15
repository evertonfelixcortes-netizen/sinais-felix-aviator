import streamlit as st
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from sklearn.ensemble import RandomForestClassifier
import time

st.title("🚀 Felix Aviator AUTO (Nível Máximo)")

# =============================
# PEGAR DADOS AUTOMÁTICO REAL
# =============================
def pegar_dados():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.tipminer.com/br/historico/sortenabet/aviator")

    time.sleep(5)

    spans = driver.find_elements("tag name", "span")

    valores = []

    for s in spans:
        txt = s.text.replace("x","").strip()
        try:
            v = float(txt)
            if 1 <= v <= 100:
                valores.append(v)
        except:
            pass

    driver.quit()
    return valores[:200]

# =============================
# IA
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

    modelo = RandomForestClassifier(n_estimators=200)
    modelo.fit(X, y)
    return modelo

# =============================
# EXECUÇÃO
# =============================
if st.button("🔄 ATUALIZAR DADOS AUTOMÁTICO"):
    dados = pegar_dados()

    if not dados:
        st.error("Erro ao pegar dados")
        st.stop()

    st.success(f"{len(dados)} dados capturados")

    modelo = treinar(dados)

    ultimos = dados[:10]

    pred = modelo.predict([ultimos])[0]

    if pred == 2:
        st.error("🔥 Buscar 10x")
    elif pred == 1:
        st.success("🟢 Entrar (2x)")
    else:
        st.warning("🔴 Evitar")

    st.write(dados[:20])
