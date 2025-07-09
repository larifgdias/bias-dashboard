import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# CONFIGURAÇÃO INICIAL
# ---------------------------

st.set_page_config(
    page_title="Simulador de Viés em Recomendação",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("🤖 Simulador de Viés em Sistemas de Recomendação")
st.markdown("""
Este simulador interativo demonstra como **viéses nos dados** — como popularidade, gênero ou classe social —  
podem afetar os resultados em **sistemas de recomendação algorítmica**.

📌 **Como funciona:**  
- À esquerda, selecione o tipo de viés que deseja aplicar.  
- Observe como os scores mudam com a aplicação desse viés.  
- Compare os gráficos lado a lado para entender o impacto.

🔎 Os dados são simulados apenas para fins educacionais.
""")

# ---------------------------
# SIMULAÇÃO DOS DADOS BASE
# ---------------------------

np.random.seed(42)
itens = [f"Item {i}" for i in range(1, 11)]
scores_originais = np.random.uniform(2, 5, size=10)

df_base = pd.DataFrame({
    "Item": itens,
    "Score Original (sem viés)": scores_originais
})

# ---------------------------
# INTERFACE DO USUÁRIO
# ---------------------------

st.sidebar.header("⚙️ Escolha um tipo de viés")
tipo_vies = st.sidebar.selectbox("Tipo de viés para simular:", ["Nenhum", "Popularidade", "Gênero", "Classe"])

# ---------------------------
# APLICAÇÃO DO VIÉS
# ---------------------------

df_simulado = df_base.copy()

if tipo_vies == "Popularidade":
    st.sidebar.markdown("📈 Este viés favorece os itens mais populares.")
    popularidade = np.linspace(1.5, 0.5, 10)  # decrescente
    df_simulado["Score com Viés"] = df_base["Score Original (sem viés)"] * popularidade

elif tipo_vies == "Gênero":
    st.sidebar.markdown("🚻 Este viés favorece itens associados a um determinado gênero.")
    generos = ['Feminino', 'Masculino'] * 5
    df_simulado["Gênero"] = generos
    df_simulado["Score com Viés"] = np.where(
        df_simulado["Gênero"] == 'Feminino',
        df_base["Score Original (sem viés)"] * 1.2,
        df_base["Score Original (sem viés)"] * 0.8
    )

elif tipo_vies == "Classe":
    st.sidebar.markdown("💸 Este viés favorece itens consumidos por pessoas de classe mais alta.")
    classe = ['Alta'] * 5 + ['Baixa'] * 5
    df_simulado["Classe"] = classe
    df_simulado["Score com Viés"] = np.where(
        df_simulado["Classe"] == 'Alta',
        df_base["Score Original (sem viés)"] * 1.3,
        df_base["Score Original (sem viés)"] * 0.7
    )

else:
    df_simulado["Score com Viés"] = df_base["Score Original (sem viés)"]

# ---------------------------
# VISUALIZAÇÃO COMPARATIVA
# ---------------------------

st.markdown("### 📊 Comparação dos Scores")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**🔹 Sem viés**")
    fig1, ax1 = plt.subplots()
    ax1.bar(df_base["Item"], df_base["Score Original (sem viés)"], color='#4da6ff')
    ax1.set_ylim(0, max(df_simulado["Score com Viés"]) * 1.2)
    ax1.set_ylabel("Score")
    st.pyplot(fig1)

with col2:
    st.markdown(f"**🔸 Com viés: {tipo_vies}**")
    fig2, ax2 = plt.subplots()
    ax2.bar(df_simulado["Item"], df_simulado["Score com Viés"], color='#ff6666')
    ax2.set_ylim(0, max(df_simulado["Score com Viés"]) * 1.2)
    ax2.set_ylabel("Score")
    st.pyplot(fig2)

# ---------------------------
# TABELA DE DADOS
# ---------------------------

with st.expander("📋 Ver tabela de dados"):
    st.dataframe(df_simulado)

# ---------------------------
# RODAPÉ
# ---------------------------

st.markdown("---")
st.markdown("""
📌 Este simulador é uma ferramenta educativa criada para demonstrar como **dados enviesados podem alterar resultados algorítmicos**.  
Todos os dados são fictícios e gerados aleatoriamente com propósitos didáticos.

Feito com ❤️ por [Larissa Dias](https://github.com/larifgdias)
""")
