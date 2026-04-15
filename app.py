import streamlit as st
import numpy as np
import json
import os
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Felix Aviator PRO", layout="centered")

st.title("🚀 Felix Aviator PRO (Nível Máximo)")

ARQ = "historico.json"

# =============================
# SALVAR DADOS
# =============================
def salvar(dados):
    with open(ARQ, "w") as f:
        json.dump(dados, f)

# =============================
# CARREGAR DADOS
# =============================
def carregar():
    if os.path.exists(ARQ):
        with open(ARQ, "r") as f:
            return json.load(f)
    return []

dados = carregar()

# =============================
# ENTRADA AUTOMÁTICA (manual assistida)
# =============================
st.subheader("📥 Inserir novo resultado")

novo = st.text_input("Digite último resultado (ex: 1.8)")

if st.button("Adicionar resultado"):
    try:
        v = float(novo)
        dados.insert(0, v)
        salvar(dados)
        st.success("Adicionado com sucesso")
    except:
        st.error("Valor inválido")

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

if len(dados) < 20:
    st.warning("⚠️ Adicione pelo menos 20 resultados")
    st.stop()

modelo = treinar(dados)

ultimos = dados[:10]

# =============================
# DETECTOR DE PADRÃO
# =============================
def padrao(d):
    baixos = sum(1 for x in d[:10] if x < 1.5)
    altos = sum(1 for x in d[:10] if x > 5)

    if baixos >= 6:
        return "SUBIDA"
    elif altos >= 3:
        return "QUEDA"
    return "NEUTRO"

# =============================
# SINAL
# =============================
if st.button("🔮 GERAR SINAL PRO"):
    p = modelo.predict([ultimos])[0]
    pad = padrao(dados)

    if p == 2 and pad == "SUBIDA":
        st.error("🔥🔥 SINAL FORTE (10x)")
    elif p == 1:
        st.success("🟢 ENTRAR (2x seguro)")
    elif pad == "QUEDA":
        st.warning("🔴 EVITAR")
    else:
        st.info("⚠️ AGUARDAR")

# =============================
# DASHBOARD
# =============================
st.subheader("📊 Estatísticas")

st.write(f"Média: {np.mean(dados):.2f}x")
st.write(f"Maior: {max(dados)}x")
st.write(f"Total: {len(dados)}")

st.write("Últimos 15:")
st.write(dados[:15])
