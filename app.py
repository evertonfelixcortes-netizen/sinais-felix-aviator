import streamlit as st
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Sinais do Felix-Aviator", layout="centered")

st.title("🚀 Sinais do Felix-Aviator")

st.write("Cole os últimos resultados (ex: 1.2, 2.5, 1.8)")

# =============================
# ENTRADA MANUAL (SEM ERRO)
# =============================
entrada = st.text_area("📋 Resultados:")

if not entrada:
    st.warning("⚠️ Cole os dados para começar")
    st.stop()

try:
    dados = [float(x.strip()) for x in entrada.split(",")]
except:
    st.error("❌ Formato errado. Use: 1.2, 2.5, 1.8")
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

if len(dados) < 10:
    st.warning("⚠️ Use pelo menos 10 valores")
    st.stop()

modelo = treinar(dados)

ultimos = dados[-5:]

# =============================
# SINAL
# =============================
if st.button("🔮 GERAR SINAL"):
    pred = modelo.predict([ultimos])[0]

    if pred == 2:
        st.error("🔥 ALTA CHANCE DE 10x (RISCO ALTO)")
    elif pred == 1:
        st.success("🟢 ENTRAR - BUSCAR 2x")
    else:
        st.warning("🔴 EVITAR ESSA RODADA")

# =============================
# ESTATÍSTICAS
# =============================
st.write("📊 Últimos dados:")
st.write(dados[-10:])

st.write(f"Média: {np.mean(dados):.2f}x")
st.write(f"Maior valor: {max(dados)}x")
