# =============================================================================
# ☄️  ASTEROID DASHBOARD — NASA-inspired dark space theme
#     Streamlit + Plotly | arquivo: app.py
# =============================================================================

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ── Configuração da página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="☄️ Asteroid Dashboard",
    page_icon="☄️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS personalizado (tema espacial) ─────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600&display=swap');

    /* Fundo geral */
    .stApp {
        background: radial-gradient(ellipse at 20% 10%, #0d0d2b 0%, #050510 60%, #000000 100%);
        font-family: 'Exo 2', sans-serif;
    }

    /* Título principal */
    h1 { font-family: 'Orbitron', sans-serif !important; letter-spacing: 3px; }
    h2, h3 { font-family: 'Orbitron', sans-serif !important; letter-spacing: 1px; }

    /* Cards de KPI */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(30,10,80,0.85) 0%, rgba(10,30,80,0.85) 100%);
        border: 1px solid rgba(130,80,255,0.45);
        border-radius: 14px;
        padding: 18px 22px;
        box-shadow: 0 0 22px rgba(100,60,255,0.25), inset 0 0 8px rgba(100,60,255,0.08);
        transition: box-shadow 0.3s;
    }
    [data-testid="metric-container"]:hover {
        box-shadow: 0 0 38px rgba(100,60,255,0.5);
    }
    [data-testid="stMetricLabel"] { color: #a78bfa !important; font-size: 0.78rem; letter-spacing: 1.5px; text-transform: uppercase; }
    [data-testid="stMetricValue"] { color: #e0d7ff !important; font-family: 'Orbitron', sans-serif; font-size: 1.6rem; }
    [data-testid="stMetricDelta"] { color: #7dd3fc !important; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a20 0%, #05050f 100%);
        border-right: 1px solid rgba(130,80,255,0.3);
    }
    [data-testid="stSidebar"] * { color: #c4b5fd !important; }

    /* Divisores */
    hr { border-color: rgba(130,80,255,0.25) !important; }

    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(30,10,80,0.6) !important;
        border: 1px solid rgba(130,80,255,0.3) !important;
        border-radius: 8px !important;
        color: #c4b5fd !important;
        font-family: 'Exo 2', sans-serif;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] { border: 1px solid rgba(130,80,255,0.3) !important; border-radius: 10px; }

    /* Seção de insights */
    .insight-card {
        background: linear-gradient(135deg, rgba(20,5,60,0.9), rgba(5,20,60,0.9));
        border: 1px solid rgba(130,80,255,0.5);
        border-left: 4px solid #7c3aed;
        border-radius: 10px;
        padding: 14px 20px;
        margin-bottom: 10px;
        color: #ddd6fe;
        font-size: 0.95rem;
    }

    /* Estrelas decorativas no fundo (pseudo-efeito via gradiente) */
    .star-header {
        text-align: center;
        padding: 6px 0 20px;
        font-family: 'Orbitron', sans-serif;
        font-size: 2rem;
        font-weight: 900;
        background: linear-gradient(90deg, #818cf8, #c084fc, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 4px;
    }
    .sub-header {
        text-align: center;
        color: #64748b;
        font-size: 0.85rem;
        letter-spacing: 2px;
        margin-top: -16px;
        margin-bottom: 28px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Constantes de cor do tema ─────────────────────────────────────────────────
CORES = {
    "roxo":     "#7c3aed",
    "roxo_claro": "#a78bfa",
    "azul":     "#3b82f6",
    "azul_claro": "#7dd3fc",
    "rosa":     "#ec4899",
    "verde":    "#34d399",
    "amarelo":  "#fbbf24",
    "fundo":    "#050510",
    "texto":    "#e0d7ff",
}

PLOTLY_TEMPLATE = dict(
    layout=go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(10,5,30,0.6)",
        font=dict(color=CORES["texto"], family="Exo 2, sans-serif"),
        xaxis=dict(gridcolor="rgba(130,80,255,0.12)", zerolinecolor="rgba(130,80,255,0.2)"),
        yaxis=dict(gridcolor="rgba(130,80,255,0.12)", zerolinecolor="rgba(130,80,255,0.2)"),
        colorway=[CORES["roxo_claro"], CORES["azul_claro"], CORES["rosa"],
                  CORES["verde"], CORES["amarelo"], CORES["azul"], CORES["roxo"]],
    )
)

# ── Carregamento e cache dos dados ────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "asteroides.csv"


@st.cache_data(show_spinner="🌌 Carregando dados do cinturão de asteroides…")
def carregar_dados() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH)
    for col in ["moid_au", "per_y", "H", "diameter_km", "albedo", "e"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["class"] = df["class"].fillna("Desconhecida")
    df["pha"] = df["pha"].astype(bool) if "pha" in df.columns else False
    df["diameter_is_estimated"] = df.get("diameter_is_estimated", False)
    return df


df_raw = carregar_dados()

# ── Helpers ───────────────────────────────────────────────────────────────────

def pct(cond: pd.Series, total: int) -> float:
    return round((cond.sum() / total) * 100, 2) if total else 0.0


def fmt_num(n: int | float) -> str:
    return f"{int(n):,}".replace(",", ".")


# ── Sidebar — Filtros ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛰️ Filtros")
    st.markdown("---")

    # Classe orbital
    classes_disp = sorted(df_raw["class"].unique().tolist())
    classes_sel = st.multiselect(
        "🪐 Classe Orbital",
        options=classes_disp,
        default=classes_disp,
        help="Selecione as classes orbitais a exibir",
    )

    # PHA
    pha_opcao = st.radio(
        "⚠️ Potencialmente Perigoso (PHA)",
        options=["Todos", "Somente perigosos", "Somente não-perigosos"],
        index=0,
    )

    # Faixa de diâmetro
    diam_min_val = float(df_raw["diameter_km"].dropna().min())
    diam_max_val = float(df_raw["diameter_km"].dropna().max())
    diam_range = st.slider(
        "📏 Diâmetro (km)",
        min_value=diam_min_val,
        max_value=diam_max_val,
        value=(diam_min_val, diam_max_val),
        step=0.1,
    )

    # Faixa de magnitude absoluta (H)
    h_min_val = float(df_raw["H"].dropna().min())
    h_max_val = float(df_raw["H"].dropna().max())
    h_range = st.slider(
        "💡 Magnitude Absoluta (H)",
        min_value=h_min_val,
        max_value=h_max_val,
        value=(h_min_val, h_max_val),
        step=0.5,
        help="Menor H = objeto mais brilhante/maior",
    )

    st.markdown("---")
    st.markdown(
        "<small style='color:#475569'>Dados: NASA JPL Small-Body Database</small>",
        unsafe_allow_html=True,
    )


# ── Aplicar filtros ───────────────────────────────────────────────────────────
df = df_raw.copy()

if classes_sel:
    df = df[df["class"].isin(classes_sel)]

if pha_opcao == "Somente perigosos":
    df = df[df["pha"] == True]
elif pha_opcao == "Somente não-perigosos":
    df = df[df["pha"] == False]

mask_diam = df["diameter_km"].isna() | (
    (df["diameter_km"] >= diam_range[0]) & (df["diameter_km"] <= diam_range[1])
)
df = df[mask_diam]

mask_h = df["H"].isna() | ((df["H"] >= h_range[0]) & (df["H"] <= h_range[1]))
df = df[mask_h]

total = len(df)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="star-header">☄️ ASTEROID DASHBOARD</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">ANÁLISE EXPLORATÓRIA · NASA SMALL-BODY DATABASE</div>',
    unsafe_allow_html=True,
)

# ── KPIs ──────────────────────────────────────────────────────────────────────
st.markdown("### 🔭 Indicadores Principais")
k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("☄️ Total de Asteroides", fmt_num(total))
k2.metric(
    "⚠️ Perigosos (PHA)",
    f"{pct(df['pha'] == True, total):.1f}%",
    delta=f"{(df['pha'] == True).sum()} objetos",
)
k3.metric(
    "🌍 Próximos da Terra",
    f"{pct(df['moid_au'] < 0.05, total):.1f}%",
    delta="MOID < 0.05 AU",
)
k4.metric(
    "⚡ Órbita Rápida",
    f"{pct(df['per_y'] < 2, total):.1f}%",
    delta="período < 2 anos",
)
k5.metric(
    "🔵 Grandes (> 1 km)",
    f"{pct(df['diameter_km'] > 1, total):.1f}%",
    delta=f"{(df['diameter_km'] > 1).sum()} objetos",
)

st.markdown("---")

# ── Linha 1: Resumo geral + Pizza de classes ──────────────────────────────────
col_bar, col_pie = st.columns([3, 2])

with col_bar:
    st.markdown("#### 📊 Resumo Percentual")

    resumo = pd.DataFrame(
        {
            "Categoria": [
                "Com nome", "Perigosos (PHA)", "Próx. Terra (MOID<0.05)",
                "Órbita rápida (<2 anos)", "Alta luminosidade (H<15)",
                "Órbita alongada (e>0.5)", "Alto albedo (>0.25)",
                "Diâm. estimado", "Grandes (>1 km)",
            ],
            "Percentual": [
                pct(df["name"].notna() & (df["name"] != ""), total),
                pct(df["pha"] == True, total),
                pct(df["moid_au"] < 0.05, total),
                pct(df["per_y"] < 2, total),
                pct(df["H"] < 15, total),
                pct(df["e"] > 0.5, total),
                pct(df["albedo"] > 0.25, total),
                pct(df["diameter_is_estimated"] == True, total),
                pct(df["diameter_km"] > 1, total),
            ],
        }
    ).sort_values("Percentual", ascending=True)

    fig_bar = go.Figure(
        go.Bar(
            x=resumo["Percentual"],
            y=resumo["Categoria"],
            orientation="h",
            marker=dict(
                color=resumo["Percentual"],
                colorscale=[[0, "#3730a3"], [0.5, "#7c3aed"], [1, "#c084fc"]],
                line=dict(color="rgba(200,150,255,0.4)", width=0.8),
            ),
            text=[f"{v:.1f}%" for v in resumo["Percentual"]],
            textposition="outside",
            textfont=dict(color="#e0d7ff", size=11),
        )
    )
    fig_bar.update_layout(
        **PLOTLY_TEMPLATE["layout"].to_plotly_json(),
        height=380,
        margin=dict(l=10, r=60, t=10, b=10),
        xaxis_title="% do total",
        yaxis_title="",
        bargap=0.25,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_pie:
    st.markdown("#### 🪐 Distribuição por Classe")

    df_cls = (
        df["class"].value_counts().reset_index()
        .rename(columns={"class": "Classe", "count": "Qtd"})
        .head(10)
    )

    fig_pie = go.Figure(
        go.Pie(
            labels=df_cls["Classe"],
            values=df_cls["Qtd"],
            hole=0.48,
            marker=dict(
                colors=[
                    "#7c3aed", "#6d28d9", "#4f46e5", "#3b82f6",
                    "#0ea5e9", "#06b6d4", "#14b8a6", "#10b981",
                    "#a78bfa", "#c084fc",
                ],
                line=dict(color="#050510", width=1.5),
            ),
            textinfo="label+percent",
            textfont=dict(size=11, color="#e0d7ff"),
            hovertemplate="<b>%{label}</b><br>%{value:,} asteroides<br>%{percent}<extra></extra>",
        )
    )
    fig_pie.update_layout(
        **PLOTLY_TEMPLATE["layout"].to_plotly_json(),
        height=380,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        annotations=[
            dict(
                text=f"<b>{fmt_num(total)}</b><br><span style='font-size:10px'>total</span>",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="#e0d7ff"),
            )
        ],
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Linha 2: Tamanho + Scatter MOID vs Diâmetro ───────────────────────────────
col_tam, col_scatter = st.columns([1, 2])

with col_tam:
    st.markdown("#### 📏 Distribuição por Tamanho")

    df_tam = pd.DataFrame(
        {
            "Categoria": ["Pequenos\n(<100m)", "Médios\n(100m–1km)", "Grandes\n(>1km)"],
            "Percentual": [
                pct(df["diameter_km"] < 0.1, total),
                pct((df["diameter_km"] >= 0.1) & (df["diameter_km"] <= 1), total),
                pct(df["diameter_km"] > 1, total),
            ],
            "Cor": [CORES["azul_claro"], CORES["roxo_claro"], CORES["rosa"]],
        }
    )

    fig_tam = go.Figure(
        go.Bar(
            x=df_tam["Categoria"],
            y=df_tam["Percentual"],
            marker_color=df_tam["Cor"],
            marker_line=dict(color="rgba(255,255,255,0.1)", width=0.5),
            text=[f"{v:.1f}%" for v in df_tam["Percentual"]],
            textposition="outside",
            textfont=dict(color="#e0d7ff", size=12),
        )
    )
    fig_tam.update_layout(
        **PLOTLY_TEMPLATE["layout"].to_plotly_json(),
        height=340,
        margin=dict(l=10, r=10, t=10, b=10),
        yaxis_title="% do total",
        xaxis_title="",
        bargap=0.35,
    )
    st.plotly_chart(fig_tam, use_container_width=True)

with col_scatter:
    st.markdown("#### 🌌 MOID vs Diâmetro (proximidade à Terra)")

    df_sc = df[df["moid_au"].notna() & df["diameter_km"].notna()].copy()
    df_sc["PHA_label"] = df_sc["pha"].map({True: "⚠️ Perigoso", False: "✅ Seguro"})

    fig_sc = px.scatter(
        df_sc.sample(min(3000, len(df_sc)), random_state=42),
        x="moid_au",
        y="diameter_km",
        color="PHA_label",
        color_discrete_map={"⚠️ Perigoso": CORES["rosa"], "✅ Seguro": CORES["azul_claro"]},
        opacity=0.65,
        hover_data={"moid_au": ":.4f", "diameter_km": ":.2f", "class": True},
        labels={"moid_au": "MOID (AU)", "diameter_km": "Diâmetro (km)", "PHA_label": "Tipo"},
        log_y=True,
    )
    fig_sc.update_traces(marker=dict(size=5, line=dict(width=0.4, color="rgba(255,255,255,0.3)")))
    fig_sc.add_vline(
        x=0.05, line_dash="dash", line_color=CORES["amarelo"],
        annotation_text="Limite NEO (0.05 AU)", annotation_font_color=CORES["amarelo"],
    )
    fig_sc.update_layout(
        **PLOTLY_TEMPLATE["layout"].to_plotly_json(),
        height=340,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=-0.18, font=dict(size=11)),
    )
    st.plotly_chart(fig_sc, use_container_width=True)

# ── Linha 3: H vs Diâmetro + Scatter excentricidade ──────────────────────────
col_hd, col_e = st.columns(2)

with col_hd:
    st.markdown("#### 💡 Magnitude Absoluta (H) vs Diâmetro")

    df_hd = df[df["H"].notna() & df["diameter_km"].notna()].copy()

    fig_hd = px.scatter(
        df_hd.sample(min(3000, len(df_hd)), random_state=7),
        x="H",
        y="diameter_km",
        color="class",
        opacity=0.55,
        log_y=True,
        labels={"H": "Magnitude Absoluta (H)", "diameter_km": "Diâmetro (km)", "class": "Classe"},
    )
    fig_hd.update_traces(marker=dict(size=4))
    fig_hd.update_layout(
        **PLOTLY_TEMPLATE["layout"].to_plotly_json(),
        height=330,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
    )
    st.plotly_chart(fig_hd, use_container_width=True)

with col_e:
    st.markdown("#### 🌀 Excentricidade Orbital por Classe")

    df_e = df[df["e"].notna() & df["class"].notna()].copy()
    top_classes = df_e["class"].value_counts().head(8).index
    df_e = df_e[df_e["class"].isin(top_classes)]

    fig_e = px.box(
        df_e,
        x="class",
        y="e",
        color="class",
        labels={"class": "Classe Orbital", "e": "Excentricidade"},
        color_discrete_sequence=[
            CORES["roxo"], CORES["azul"], CORES["rosa"], CORES["verde"],
            CORES["amarelo"], CORES["azul_claro"], CORES["roxo_claro"], CORES["texto"],
        ],
    )
    fig_e.add_hline(
        y=1.0, line_dash="dot", line_color=CORES["rosa"],
        annotation_text="e=1 (parabólica)", annotation_font_color=CORES["rosa"],
    )
    fig_e.update_layout(
        **PLOTLY_TEMPLATE["layout"].to_plotly_json(),
        height=330,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
    )
    st.plotly_chart(fig_e, use_container_width=True)

# ── Insights automáticos ──────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🤖 Insights Automáticos")

insights = []

pct_pha = pct(df["pha"] == True, total)
if pct_pha > 5:
    insights.append(
        f"🚨 <b>{pct_pha:.1f}%</b> dos asteroides filtrados são classificados como "
        "Potencialmente Perigosos (PHA) — acima do limiar de atenção de 5%."
    )
elif pct_pha > 0:
    insights.append(
        f"✅ Apenas <b>{pct_pha:.1f}%</b> dos asteroides filtrados são Potencialmente "
        "Perigosos (PHA). O risco imediato é baixo dentro desta seleção."
    )

pct_moid = pct(df["moid_au"] < 0.05, total)
insights.append(
    f"🌍 <b>{pct_moid:.1f}%</b> dos asteroides têm MOID inferior a 0.05 AU, "
    "passando dentro da zona de monitoramento próxima à Terra."
)

classe_dom = df["class"].value_counts().idxmax() if total > 0 else "N/A"
pct_cls = pct(df["class"] == classe_dom, total)
insights.append(
    f"🪐 A classe orbital dominante é <b>{classe_dom}</b>, representando "
    f"<b>{pct_cls:.1f}%</b> dos asteroides nesta seleção."
)

pct_grandes = pct(df["diameter_km"] > 1, total)
if pct_grandes > 10:
    insights.append(
        f"☄️ <b>{pct_grandes:.1f}%</b> dos asteroides têm diâmetro superior a 1 km — "
        "um número relevante de objetos de grande porte."
    )

mediana_h = df["H"].median() if df["H"].notna().any() else None
if mediana_h is not None:
    insights.append(
        f"💡 A mediana de magnitude absoluta (H) é <b>{mediana_h:.1f}</b>. "
        "Valores menores indicam objetos maiores e mais brilhantes."
    )

pct_est = pct(df["diameter_is_estimated"] == True, total)
insights.append(
    f"📐 <b>{pct_est:.1f}%</b> dos diâmetros são estimados (não medidos diretamente), "
    "o que indica limitações observacionais para uma parcela significativa dos objetos."
)

pct_rapidos = pct(df["per_y"] < 2, total)
insights.append(
    f"⚡ <b>{pct_rapidos:.1f}%</b> dos asteroides completam sua órbita em menos de 2 anos, "
    "indicando trajetórias internas ao cinturão principal."
)

cols_insight = st.columns(2)
for i, texto in enumerate(insights):
    with cols_insight[i % 2]:
        st.markdown(f'<div class="insight-card">{texto}</div>', unsafe_allow_html=True)

# ── Dados brutos ──────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("🗄️ Visualizar amostra dos dados filtrados"):
    colunas_exibir = [
        c for c in ["name", "class", "pha", "H", "diameter_km",
                    "moid_au", "per_y", "e", "albedo"]
        if c in df.columns
    ]
    st.dataframe(
        df[colunas_exibir].head(200).reset_index(drop=True),
        use_container_width=True,
    )
    st.caption(f"Exibindo até 200 de {fmt_num(total)} registros filtrados.")

# ── Rodapé ────────────────────────────────────────────────────────────────────
st.markdown(
    "<br><div style='text-align:center;color:#334155;font-size:0.78rem;letter-spacing:1px'>"
    "☄️ ASTEROID DASHBOARD · Dados: NASA JPL Small-Body Database · "
    "Desenvolvido com Streamlit & Plotly</div><br>",
    unsafe_allow_html=True,
)