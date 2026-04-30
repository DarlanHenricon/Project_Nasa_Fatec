import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
from pathlib import Path

# Configuração da página
st.set_page_config(page_title="Análise de Asteroides", layout="wide")

# Sidebar com menu
with st.sidebar:
    st.title("📊 Menu de Navegação")
    st.markdown("---")
    
    # Botão para asteroides perigosos
    botao_perigosos = st.button("☄️ Asteroides Perigosos", use_container_width=True)
    
    # Outros botões (exemplo para futuro)
    st.markdown("---")
    st.caption("Desenvolvido com ❤️ para ciência de dados")
    
    # Opção de upload de arquivo (caso queira mudar o CSV)
    uploaded_file = st.file_uploader("Ou faça upload do CSV:", type=["csv"])

# Carregar dados (prioriza upload do usuário ou arquivo padrão)
@st.cache_data
def carregar_dados(arquivo=None):
    if arquivo is not None:
        df = pd.read_csv(arquivo, low_memory=False)
    else:
        pasta_atual = Path(__file__).parent
        arquivo_padrao = pasta_atual / "asteroides 2025.csv"
        if not arquivo_padrao.exists():
            arquivo_padrao = pasta_atual / "asteroides.csv"
        df = pd.read_csv(arquivo_padrao, low_memory=False)
    
    # Tratamento dos dados
    df['per_y'] = pd.to_numeric(df['per_y'], errors='coerce')
    df['H'] = pd.to_numeric(df['H'], errors='coerce')
    df['diameter_km'] = pd.to_numeric(df['diameter_km'], errors='coerce')
    
    return df

# Carregar dados
df = carregar_dados(uploaded_file if uploaded_file is not None else None)

# Processamento dos dados específicos
asteroides_brilhantes_rapidos_perigosos = df[
    (df['name'].notna()) &
    (df['name'] != "") &
    (df['H'] < 15) &
    (df['pha'] == True)
].copy()

asteroides_brilhantes_rapidos_perigosos = asteroides_brilhantes_rapidos_perigosos.sort_values('H')

# PÁGINA PRINCIPAL
st.title("🚀 Análise de Asteroides Potencialmente Perigosos")
st.markdown("---")

# Verifica se o botão foi clicado
if botao_perigosos:
    st.success("✅ **Botão acionado!** Exibindo análise de asteroides perigosos, brilhantes e de órbita rápida.")
    
    # Métricas importantes
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de asteroides analisados", len(df))
    with col2:
        st.metric("Asteroides perigosos (PHA)", df['pha'].sum() if df['pha'].dtype == 'bool' else (df['pha'] == True).sum())
    with col3:
        st.metric("Asteroides brilhantes + perigosos", len(asteroides_brilhantes_rapidos_perigosos))
    
    st.markdown("---")
    
    # Tabela dos principais asteroides
    st.subheader("📋 Top 10 Asteroides Brilhantes, Rápidos e Perigosos")
    st.dataframe(
        asteroides_brilhantes_rapidos_perigosos[['name', 'H', 'diameter_km', 'pha', 'per_y']].head(10),
        use_container_width=True
    )
    
    # GRÁFICO 1: Magnitude vs Diâmetro
    st.subheader("📈 Gráfico 1: Magnitude Absoluta vs Diâmetro")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    scatter = ax1.scatter(
        asteroides_brilhantes_rapidos_perigosos['H'],
        asteroides_brilhantes_rapidos_perigosos['diameter_km'],
        c=asteroides_brilhantes_rapidos_perigosos['diameter_km'],
        cmap='viridis',
        s=100,
        alpha=0.7,
        edgecolors='black',
        linewidth=0.5
    )
    ax1.set_xlabel('Magnitude Absoluta (H) → menor H = mais brilhante')
    ax1.set_ylabel('Diâmetro estimado (km)')
    ax1.set_title('Asteroides Perigosos e Brilhantes (H < 15)')
    ax1.grid(True, linestyle='--', alpha=0.6)
    plt.colorbar(scatter, ax=ax1, label='Diâmetro (km)')
    st.pyplot(fig1)
    
    # GRÁFICO 2: Distribuição do período orbital
    st.subheader("📊 Gráfico 2: Distribuição do Período Orbital")
    df_compare = df.dropna(subset=['per_y', 'pha'])
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    
    # Separar dados por categoria
    perigosos = df_compare[df_compare['pha'] == True]['per_y']
    nao_perigosos = df_compare[df_compare['pha'] != True]['per_y']
    
    ax2.hist(nao_perigosos, bins=30, alpha=0.5, label='Não perigosos', color='blue', density=True)
    ax2.hist(perigosos, bins=30, alpha=0.5, label='Perigosos (PHA)', color='red', density=True)
    
    ax2.set_xlabel('Período orbital (anos)')
    ax2.set_ylabel('Densidade')
    ax2.set_title('Distribuição do Período Orbital: Perigosos vs Não Perigosos')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.4)
    ax2.set_xlim(0, 20)
    
    st.pyplot(fig2)
    
    # GRÁFICO 3: Boxplot de períodos
    st.subheader("📦 Gráfico 3: Comparação de Períodos Orbitais")
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    
    dados_boxplot = [
        nao_perigosos.dropna(),
        perigosos.dropna()
    ]
    
    bp = ax3.boxplot(dados_boxplot, labels=['Não perigosos', 'Perigosos'], patch_artist=True)
    bp['boxes'][0].set_facecolor('lightblue')
    bp['boxes'][1].set_facecolor('salmon')
    
    ax3.set_ylabel('Período orbital (anos)')
    ax3.set_title('Comparação de Períodos Orbitais')
    ax3.grid(True, linestyle='--', alpha=0.3)
    
    st.pyplot(fig3)
    
    # Informações extras
    with st.expander("ℹ️ Sobre os critérios de filtro"):
        st.markdown("""
        - **Asteroides Perigosos (PHA)**: `pha == True`
        - **Brilhantes**: Magnitude absoluta `H < 15`
        - **Rápidos**: Período orbital `per_y < 2 anos`
        - **Nomeados**: Possuem nome registrado
        """)
    
else:
    # Mensagem inicial quando nenhum botão foi clicado
    st.info("👈 **Clique no botão 'Asteroides Perigosos' no menu lateral para exibir os gráficos e análises.**")
    
    # Mostrar prévia dos dados
    with st.expander("📁 Prévia dos dados carregados (primeiras linhas)"):
        st.dataframe(df.head(20), use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 🧠 Sobre este dashboard")
    st.markdown("""
    Este dashboard interativo permite visualizar:
    - 📊 Distribuição de períodos orbitais
    - 💎 Relação entre magnitude e diâmetro
    - 📦 Comparação estatística entre asteroides perigosos e não perigosos
    
    **Clique no botão no menu à esquerda para começar!**
    """)
