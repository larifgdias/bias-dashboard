import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Simulador de Viés em Sistemas Algorítmicos")

st.markdown("""
Este dashboard interativo simula como diferentes tipos de viés, como o viés de popularidade, gênero e classe, podem influenciar as recomendações feitas por sistemas algorítmicos.  
Use os controles abaixo para ajustar os parâmetros e visualizar como os dados enviesados impactam os resultados.  
""")

# Sidebar com mini tutorial
st.sidebar.header("Como usar")
st.sidebar.markdown("""
1. Selecione o viés que deseja simular.  
2. Ajuste os parâmetros relacionados a cada viés.  
3. Observe os gráficos para entender o impacto do viés nas recomendações.  
4. Experimente combinar diferentes vieses para ver efeitos cumulativos.
""")

# Seleção do tipo de viés
bias_type = st.selectbox("Selecione o tipo de viés para simular:", 
                         ["Viés de Popularidade", "Viés de Gênero", "Viés de Classe"])

# Exemplo simples de parâmetros para cada viés
if bias_type == "Viés de Popularidade":
    popularity_threshold = st.slider("Limite mínimo de popularidade para recomendação:", 0, 100, 50)
elif bias_type == "Viés de Gênero":
    gender_bias_strength = st.slider("Força do viés de gênero (0 = nenhum, 1 = total):", 0.0, 1.0, 0.5)
elif bias_type == "Viés de Classe":
    class_bias_strength = st.slider("Força do viés de classe (0 = nenhum, 1 = total):", 0.0, 1.0, 0.5)

# Simulação simples de dados
np.random.seed(42)
data = pd.DataFrame({
    "Item": [f"Item {i}" for i in range(1, 21)],
    "Popularidade": np.random.randint(0, 100, 20),
    "Gênero Preferido": np.random.choice(["Masculino", "Feminino"], 20),
    "Classe Social": np.random.choice(["Alta", "Média", "Baixa"], 20),
    "Score": np.random.rand(20)
})

# Aplicar filtro/simulação do viés selecionado
if bias_type == "Viés de Popularidade":
    filtered_data = data[data["Popularidade"] >= popularity_threshold]
    st.write(f"Itens com popularidade maior ou igual a {popularity_threshold}:")
    st.dataframe(filtered_data)
elif bias_type == "Viés de Gênero":
    # Simula redução de score para gênero "Feminino" conforme força do viés
    data["Score Ajustado"] = data.apply(lambda row: row["Score"] * (1 - gender_bias_strength) if row["Gênero Preferido"] == "Feminino" else row["Score"], axis=1)
    st.write("Scores ajustados considerando viés de gênero:")
    st.dataframe(data[["Item", "Gênero Preferido", "Score", "Score Ajustado"]])
elif bias_type == "Viés de Classe":
    # Simula redução de score para classes baixas conforme força do viés
    data["Score Ajustado"] = data.apply(lambda row: row["Score"] * (1 - class_bias_strength) if row["Classe Social"] == "Baixa" else row["Score"], axis=1)
    st.write("Scores ajustados considerando viés de classe:")
    st.dataframe(data[["Item", "Classe Social", "Score", "Score Ajustado"]])

# Gráfico exemplo: comparação entre score original e ajustado
if bias_type in ["Viés de Gênero", "Viés de Classe"]:
    fig, ax = plt.subplots(figsize=(10,5))
    ax.bar(data["Item"], data["Score"], alpha=0.6, label="Score Original")
    ax.bar(data["Item"], data["Score Ajustado"], alpha=0.6, label="Score Ajustado")
    ax.set_xticklabels(data["Item"], rotation=45, ha="right")
    ax.set_ylabel("Score")
    ax.set_title(f"Comparação Scores - {bias_type}")
    ax.legend()
    st.pyplot(fig)