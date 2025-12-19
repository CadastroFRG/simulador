import streamlit as st
import pandas as pd
import locale
from io import BytesIO

# Função para formatar valores em reais no formato brasileiro (Versão Universal)
def formatar_reais(valor):
    """
    Formata valor monetário no padrão brasileiro (R$ 1.234,56)
    Funciona em Windows e Linux (Streamlit Cloud) sem depender de locale.
    """
    if valor is None:
        return "R$ 0,00"
    
    # 1. Formata com padrão americano: 1,234.56
    valor_formatado = f"{valor:,.2f}"
    
    # 2. Inverte os separadores usando um caractere temporário (X)
    # Vírgula (milhar) vira Ponto
    # Ponto (decimal) vira Vírgula
    valor_formatado = valor_formatado.replace(",", "X").replace(".", ",").replace("X", ".")
    
    return f"R$ {valor_formatado}"

# Função para formatar números (não moedas) caso precise
def formatar_numero(valor, casas_decimais=2):
    format_str = f"{{:,.{casas_decimais}f}}"
    v = format_str.format(valor)
    return v.replace(",", "X").replace(".", ",").replace("X", ".")

# Função para converter DataFrame para Excel em memória
def converter_para_excel(df):
    """Converte um DataFrame para um arquivo Excel em memória"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Resumo')
    output.seek(0)
    return output

# Configurar página com CSS personalizado
st.set_page_config(
    page_title="Simulador de Contribuição Esporádica - FRG",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado para estilo FRG - CORRIGIDO (cores verdes alteradas para vermelho/bordô)
st.markdown("""
<style>
    /* Estilos gerais inspirados no site da FRG */
    .main {
        background-color: #f8f9fa;
    }
    
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Cabeçalho estilo FRG */
    .header-frg {
        background: linear-gradient(135deg, #8b043b 0%, #69042a 100%);
        color: white;
        padding: 2rem 1rem;
        border-radius: 0 0 10px 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Cards estilo FRG */
    .card-frg {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #69042a;
        margin-bottom: 1.5rem;
    }
    
    .card-title {
        color: #8b043b;
        font-weight: 600;
        font-size: 1.2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #e9ecef;
        padding-bottom: 0.5rem;
    }
    
    /* Botões estilo FRG */
    .stButton > button {
        background: linear-gradient(135deg, #8b043b 0%, #69042a 100%);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #6a032d 0%, #4d031f 100%); /* Corrigido: vermelho mais escuro */
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(139, 4, 59, 0.2); /* Corrigido: vermelho no box-shadow */
    }
    
    /* Sliders estilo FRG */
    .stSlider > div > div > div {
        background-color: #69042a !important;
    }
    
    /* Métricas estilo FRG */
    .stMetric {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    }
    
    .stMetric > div > div {
        color: #8b043b !important;
        font-weight: 700 !important;
    }
    
    .stMetric label {
        color: #495057 !important;
        font-weight: 600 !important;
    }
    
    /* Divisores */
    .stDivider {
        margin: 2rem 0 !important;
    }
    
    /* Tabela estilo FRG */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    .dataframe thead {
        background-color: #8b043b !important;
        color: white !important;
    }
    
    /* Avisos e informações */
    .stAlert {
        border-radius: 8px;
    }
    
    /* Progress bar estilo FRG */
    .stProgress > div > div > div {
        background-color: #69042a !important;
    }
    
    /* Inputs estilo FRG */
    .stNumberInput input {
        border: 2px solid #e9ecef;
        border-radius: 6px;
    }
    
    .stNumberInput input:focus {
        border-color: #69042a;
        box-shadow: 0 0 0 0.2rem rgba(139, 4, 59, 0.25); /* Corrigido: vermelho no box-shadow */
    }
    
    /* Badges para valores fixos - CORRIGIDO (verde para vermelho) */
    .badge-frg {
        background-color: #f9e9ef;  /* Vermelho claro */
        color: #8b043b;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        border: 1px solid #e6b8c6;  /* Borda vermelha clara */
    }
    
    /* Classes para backgrounds vermelhos */
    .bg-frg-light {
        background-color: #f9e9ef !important;  /* Vermelho muito claro */
    }
    
    .bg-frg-lighter {
        background-color: #fcf2f6 !important;  /* Vermelho super claro */
    }
    
    .bg-frg-soft {
        background-color: #f5d8e2 !important;  /* Vermelho suave */
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho estilo FRG
st.markdown("""
<div class="header-frg">
    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
        <div style="flex: 1;">
            <h1 style="margin: 0; font-size: 2rem; font-weight: 700;">Simulador de Contribuição Esporádica</h1>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">
                Fundação de Previdência Real Grandeza
            </p>
        </div>
        <div style="font-size: 0.9rem; text-align: right; opacity: 0.8;">
            <div>Incentivo Fiscal 2025</div>
            <div>Prazo: até 31/12/2025</div>
        </div>
    </div>
    <p style="margin: 0; font-size: 1rem; opacity: 0.9;">
        Simule sua contribuição esporádica e maximize seu benefício fiscal
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="card-frg">', unsafe_allow_html=True)
st.markdown('<div class="card-title">📋 Informações para Simulação</div>', unsafe_allow_html=True)
st.markdown("""
<p style="color: #6c757d; margin-bottom: 1.5rem;">
    <strong>Instruções:</strong> Preencha os dados abaixo para simular sua contribuição. 
    Os campos destacados são obrigatórios para o cálculo.
</p>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Layout principal com colunas
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="card-frg">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">💰 Dados de Entrada</div>', unsafe_allow_html=True)
    
    # Informações básicas
    salario_mensal = st.number_input(
        "**Salário Mensal (R$)**",
        min_value=0.0,
        value=10000.0,
        step=100.0,
        format="%.2f",
        help="Informe seu salário mensal bruto"
    )
    
    salario_anual = salario_mensal * 14
    
    st.markdown(f"""
    <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px; margin: 1rem 0;">
        <div style="font-size: 0.9rem; color: #6c757d;">Salário Anual estimado (14× incluindo PLR)</div>
        <div style="font-size: 1.5rem; font-weight: 700; color: #8b043b;">{formatar_reais(salario_anual)}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # CORRIGIDO: #f0f9f4 (verde) para #fcf2f6 (vermelho super claro)
    st.markdown("""
    <div style="margin: 1.5rem 0 1rem 0; padding: 1rem; background: #fcf2f6; border-radius: 6px; border-left: 3px solid #69042a;">
        <div style="font-size: 0.85rem; color: #8b043b; font-weight: 600;">
            ℹ️ Contribuição básica = Parcela A + Parcela B (Item 5.1.1 do Regulamento)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1a, col1b = st.columns(2)
    
    with col1a:
        contribuicao_basica_pct = st.slider(
            "**Contribuição Básica A (%)**",
            min_value=0.0,
            max_value=100.0,
            value=2.0,
            step=0.1,
            format="%.1f%%",
            help="Parcela A da contribuição básica"
        )
        contribuicao_basica = contribuicao_basica_pct / 100
        valor_basica = salario_mensal * contribuicao_basica
        st.caption(f"**Valor mensal:** {formatar_reais(valor_basica)}")
        
    with col1b:
        contribuicao_basica_outro_pct = st.slider(
            "**Contribuição Básica B (%)**",
            min_value=4.5,
            max_value=10.0,
            value=10.0,
            step=0.5,
            format="%.1f%%",
            help="Parcela B da contribuição básica"
        )
        contribuicao_basica_outro = contribuicao_basica_outro_pct / 100
        
        # Valores fixos para UR
        VALOR_UR_FIXO = 795.68
        QUANTIDADE_UR_FIXA = 7
        
        valor_outro = 0 if salario_mensal < (QUANTIDADE_UR_FIXA * VALOR_UR_FIXO) else (salario_mensal - (QUANTIDADE_UR_FIXA * VALOR_UR_FIXO)) * contribuicao_basica_outro
        st.caption(f"**Valor mensal:** {formatar_reais(valor_outro)}")
    
    # Cálculo da contribuição básica mensal
    if (salario_mensal - (QUANTIDADE_UR_FIXA * VALOR_UR_FIXO)) < 0:
        valor_base = 0
    else:
        valor_base = (salario_mensal - (QUANTIDADE_UR_FIXA * VALOR_UR_FIXO)) * contribuicao_basica_outro
    
    contribuicao_mensal_sem_voluntaria = (salario_mensal * contribuicao_basica) + valor_base
    
    # CORRIGIDO: #e9f7ef (verde) para #f9e9ef (vermelho claro) e #b8e6cb para #e6b8c6
    st.markdown(f"""
    <div style="background: #f9e9ef; padding: 1rem; border-radius: 6px; margin: 1.5rem 0; border: 1px solid #e6b8c6;">
        <div style="font-size: 0.9rem; color: #8b043b;">Contribuição Básica Mensal</div>
        <div style="font-size: 1.8rem; font-weight: 700; color: #8b043b; text-align: center;">{formatar_reais(contribuicao_mensal_sem_voluntaria)}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card-frg">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">⚙️ Parâmetros do Plano</div>', unsafe_allow_html=True)
    
    # UR - valores fixos
    
    st.markdown(f"""
    <div style="margin-bottom: 1.5rem;">
        <div style="font-size: 0.9rem; color: #6c757d; margin-bottom: 0.5rem;">Unidades de Referência (UR)</div>
        <div style="display: flex; gap: 1rem;">
            <div style="flex: 1; text-align: center; background: #f8f9fa; padding: 1rem; border-radius: 6px;">
                <div style="font-size: 0.8rem; color: #6c757d;">Quantidade</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #8b043b;">7</div>
                <div class="badge-frg" style="margin-top: 0.5rem; font-size: 0.7rem;">FIXO</div>
            </div>
            <div style="flex: 1; text-align: center; background: #f8f9fa; padding: 1rem; border-radius: 6px;">
                <div style="font-size: 0.8rem; color: #6c757d;">Valor da UR</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #8b043b;">{formatar_reais(VALOR_UR_FIXO)}</div>
                <div class="badge-frg" style="margin-top: 0.5rem; font-size: 0.7rem;">FIXO</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    total_ur = QUANTIDADE_UR_FIXA * VALOR_UR_FIXO
    
    # CORRIGIDO: #f0f9f4 (verde) para #fcf2f6 (vermelho super claro)
    st.markdown(f"""
    <div style="background: #fcf2f6; padding: 1rem; border-radius: 6px; margin: 1rem 0;">
        <div style="font-size: 0.9rem; color: #8b043b;">Valor total das UR</div>
        <div style="font-size: 1.5rem; font-weight: 700; color: #8b043b;">{formatar_reais(total_ur)}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Contribuição voluntária
    # CORRIGIDO: #f0f9f4 (verde) para #fcf2f6 (vermelho super claro)
    st.markdown("""
    <div style="margin: 1.5rem 0 1rem 0; padding: 1rem; background: #fcf2f6; border-radius: 6px; border-left: 3px solid #69042a;">
        <div style="font-size: 0.85rem; color: #8b043b; font-weight: 600;">
            ℹ️ Contribuição Voluntária (Item 5.1.2 do Regulamento)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    contribuicao_voluntaria_pct = st.slider(
        "**Contribuição Voluntária (%)**",
        min_value=0.0,
        max_value=10.0,
        value=0.0,
        step=1.0,
        format="%.1f%%",
        help="Percentual de contribuição voluntária sobre o salário"
    )
    contribuicao_voluntaria_valor = salario_mensal * contribuicao_voluntaria_pct / 100
    
    st.caption(f"**Valor mensal:** {formatar_reais(contribuicao_voluntaria_valor)}")
    
    # Contribuição mensal total
    contribuicao_mensal_total = contribuicao_mensal_sem_voluntaria + contribuicao_voluntaria_valor
    
    # CORRIGIDO: #e9f7ef (verde) para #f9e9ef (vermelho claro) e #b8e6cb para #e6b8c6
    st.markdown(f"""
    <div style="background: #f9e9ef; padding: 1rem; border-radius: 6px; margin: 1.5rem 0; border: 1px solid #e6b8c6;">
        <div style="font-size: 0.9rem; color: #8b043b;">Contribuição Mensal Total</div>
        <div style="font-size: 1.8rem; font-weight: 700; color: #8b043b; text-align: center;">{formatar_reais(contribuicao_mensal_total)}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quantidade de contribuições no ano
    quantidade_contribuicoes = st.slider(
        "**Quantidade de contribuições realizadas no ano**",
        min_value=0,
        max_value=13,
        value=13,
        step=1,
        help="Número de vezes que contribuiu ao longo do ano"
    )
    
    # Total anual e percentual
    total_contribuicao_anual = contribuicao_mensal_total * quantidade_contribuicoes
    percentual_recolhido = total_contribuicao_anual / salario_anual if salario_anual > 0 else 0
    
    st.markdown(f"""
    <div style="display: flex; gap: 1rem; margin: 1.5rem 0;">
        <div style="flex: 1; background: #f8f9fa; padding: 1rem; border-radius: 6px;">
            <div style="font-size: 0.8rem; color: #6c757d;">Total Anual</div>
            <div style="font-size: 1.4rem; font-weight: 700; color: #8b043b;">{formatar_reais(total_contribuicao_anual)}</div>
        </div>
        <div style="flex: 1; background: #f8f9fa; padding: 1rem; border-radius: 6px;">
            <div style="font-size: 0.8rem; color: #6c757d;">Percentual Atual</div>
            <div style="font-size: 1.4rem; font-weight: 700; color: #8b043b;">{percentual_recolhido:.2%}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Seção de contribuição esporádica
st.markdown('<div class="card-frg">', unsafe_allow_html=True)
st.markdown('<div class="card-title">🎯 Contribuição Esporádica para Benefício Fiscal</div>', unsafe_allow_html=True)

percentual_maximo = 0.12
valor_minimo_esporadica = 3 * VALOR_UR_FIXO
valor_maximo_esporadica = salario_mensal * 5

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <div style="font-size: 1rem; color: #8b043b; font-weight: 600; margin-bottom: 1rem;">📏 Limites de Contribuição</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px; margin: 0.5rem 0;">
        <div style="font-size: 0.85rem; color: #6c757d;">Percentual Máximo para Benefício Fiscal</div>
        <div style="font-size: 1.2rem; font-weight: 700; color: #8b043b;">12%</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px; margin: 0.5rem 0;">
        <div style="font-size: 0.85rem; color: #6c757d;">Valor Mínimo (3 × UR)</div>
        <div style="font-size: 1.2rem; font-weight: 700; color: #8b043b;">{formatar_reais(valor_minimo_esporadica)}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px; margin: 0.5rem 0;">
        <div style="font-size: 0.85rem; color: #6c757d;">Valor Máximo (5 × Salário)</div>
        <div style="font-size: 1.2rem; font-weight: 700; color: #8b043b;">{formatar_reais(valor_maximo_esporadica)}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <div style="font-size: 1rem; color: #8b043b; font-weight: 600; margin-bottom: 1rem;">🎯 Contribuição Ideal Sugerida</div>
    </div>
    """, unsafe_allow_html=True)
    
    valor_ideal_esporadica = (percentual_maximo - percentual_recolhido) * salario_anual
    
    if valor_ideal_esporadica > 0:
        # CORRIGIDO: #e9f7ef (verde) para #f9e9ef (vermelho claro)
        st.markdown(f"""
        <div style="background: #f9e9ef; padding: 1.5rem; border-radius: 8px; margin: 0.5rem 0; border: 2px solid #69042a;">
            <div style="font-size: 0.9rem; color: #8b043b; margin-bottom: 0.5rem;">Valor para atingir 12% do limite fiscal</div>
            <div style="font-size: 2rem; font-weight: 700; color: #8b043b; text-align: center;">{formatar_reais(valor_ideal_esporadica)}</div>
            <div style="font-size: 0.8rem; color: #6c757d; text-align: center; margin-top: 0.5rem;">
                Aplicando este valor, você aproveitará 100% do benefício fiscal
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if valor_ideal_esporadica < valor_minimo_esporadica:
            st.warning(f"**Atenção:** O valor ideal está abaixo do mínimo permitido de {formatar_reais(valor_minimo_esporadica)}")
        elif valor_ideal_esporadica > valor_maximo_esporadica:
            st.warning(f"**Atenção:** O valor ideal está acima do máximo permitido de {formatar_reais(valor_maximo_esporadica)}")
    else:
        # CORRIGIDO: #d4edda (verde) para #e6d4da (vermelho suave) e #c3e6cb para #d4c3c6
        st.markdown("""
        <div style="background: #e6d4da; padding: 1.5rem; border-radius: 8px; margin: 0.5rem 0; border: 2px solid #d4c3c6;">
            <div style="font-size: 1.1rem; color: #8b043b; font-weight: 600; text-align: center;">
                🎉 Parabéns! Você já atingiu ou ultrapassou o percentual máximo para benefício fiscal.
            </div>
            <div style="font-size: 0.9rem; color: #8b043b; text-align: center; margin-top: 0.5rem;">
                Não é necessário realizar contribuição esporádica para aproveitar o benefício fiscal.
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Seção para contribuição personalizada
st.markdown('<div class="card-frg">', unsafe_allow_html=True)
st.markdown('<div class="card-title">💡 Contribuição Esporádica Personalizada</div>', unsafe_allow_html=True)

st.markdown("""
<p style="color: #6c757d; margin-bottom: 1.5rem;">
    Caso deseje realizar um valor de contribuição diferente do sugerido, ajuste o valor abaixo:
</p>
""", unsafe_allow_html=True)

valor_esporadica_personalizado = st.slider(
    "**Valor da Contribuição Esporádica (R$)**",
    min_value=2387.04,
    max_value=float(valor_maximo_esporadica * 1.1),
    value=5000.0,
    step=50.0,
    format="%.0f",
    help="Ajuste o valor conforme sua necessidade"
)

# Cálculos finais
if valor_esporadica_personalizado != 0:
    total_final = valor_esporadica_personalizado + total_contribuicao_anual
else:
    total_final = total_contribuicao_anual

novo_percentual = total_final / salario_anual if salario_anual > 0 else 0
progresso = min(novo_percentual / percentual_maximo, 1.0)

st.markdown(f"""
<div style="display: flex; gap: 1rem; margin: 2rem 0;">
    <div style="flex: 1; background: #f8f9fa; padding: 1.5rem; border-radius: 8px;">
        <div style="font-size: 0.9rem; color: #6c757d;">Total Final Anual</div>
        <div style="font-size: 1.8rem; font-weight: 700; color: #8b043b;">{formatar_reais(total_final)}</div>
    </div>
    <div style="flex: 1; background: #f8f9fa; padding: 1.5rem; border-radius: 8px;">
        <div style="font-size: 0.9rem; color: #6c757d;">Novo Percentual</div>
        <div style="font-size: 1.8rem; font-weight: 700; color: #8b043b;">{novo_percentual:.2%}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Barra de progresso
st.markdown(f"""
<div style="margin: 1.5rem 0;">
    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
        <span style="font-size: 0.9rem; color: #6c757d;">Progresso do limite fiscal</span>
        <span style="font-size: 0.9rem; font-weight: 600; color: #8b043b;">{progresso:.0%}</span>
    </div>
""", unsafe_allow_html=True)
st.progress(progresso)

st.markdown("""
<div style="margin-top: 1rem;">
""", unsafe_allow_html=True)

if novo_percentual <= percentual_maximo:
    st.success(f"✅ **Dentro do limite:** Seu percentual de {novo_percentual:.2%} está dentro do limite de 12% para benefício fiscal.")
else:
    st.warning(f"⚠️ **Atenção:** Seu percentual de {novo_percentual:.2%} ultrapassa o limite de 12% para benefício fiscal.")

st.markdown("""
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Continuação do código anterior...

st.markdown("""
<div style="background: #d1ecf1; padding: 1.5rem; border-radius: 8px; margin: 2rem 0; border: 1px solid #bee5eb;">
    <div style="display: flex; align-items: start; gap: 1rem;">
        <div style="font-size: 1.5rem;">💰</div>
        <div style="flex: 1;">
            <h4 style="margin: 0 0 0.5rem 0; color: #0c5460;">Benefício Fiscal Disponível</h4>
            <p style="margin: 0; color: #0c5460;">
                Se você aplicar até 12% da sua renda bruta anual tributável em um plano de Previdência Privada, 
                esse valor pode ser <strong>deduzido na sua declaração de Imposto de Renda</strong>, fazendo com 
                que você pague menos impostos no ano em que fizer o investimento.
            </p>
            <div style="margin-top: 1rem; padding: 0.75rem; background: white; border-radius: 6px; border-left: 3px solid #0c5460;">
                <div style="font-size: 0.9rem; color: #0c5460; font-weight: 600;">
                    ⏰ Prazo para Contribuição: <span style="color: #8b043b;">31/12/2025</span>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Resumo em formato de tabela
st.markdown('<div class="card-frg">', unsafe_allow_html=True)
st.markdown('<div class="card-title">📊 Resumo Completo da Simulação</div>', unsafe_allow_html=True)

# Criando DataFrame com estilo
resumo_data = {
    "Descrição": [
        "Salário Mensal",
        "Salário Anual estimado (14× incluindo PLR)",
        "Contribuição Básica A (%)",
        "Contribuição Básica B (%)",
        "Contribuição Voluntária (%)",
        "Contribuição Voluntária (R$)",
        "Quantidade de UR (fixo)",
        "Valor da UR (fixo)",
        "Valor total das UR",
        "Contribuição Básica Mensal",
        "Contribuição Mensal Total",
        "Contribuições no Ano",
        "Total Contribuído no Ano",
        "Percentual Atual",
        "Valor Esporádica Sugerido",
        "Valor Esporádica Personalizado",
        "Total Final Anual",
        "Percentual Final"
    ],
    "Valor": [
        formatar_reais(salario_mensal),
        formatar_reais(salario_anual),
        f"{contribuicao_basica_pct:.1f}%".replace(".", ","),
        f"{contribuicao_basica_outro_pct:.1f}%".replace(".", ","),
        f"{contribuicao_voluntaria_pct:.1f}%".replace(".", ","),
        formatar_reais(contribuicao_voluntaria_valor),
        f"{QUANTIDADE_UR_FIXA}",
        formatar_reais(VALOR_UR_FIXO),
        formatar_reais(total_ur),
        formatar_reais(contribuicao_mensal_sem_voluntaria),
        formatar_reais(contribuicao_mensal_total),
        f"{quantidade_contribuicoes}",
        formatar_reais(total_contribuicao_anual),
        f"{percentual_recolhido:.2%}".replace(".", ","),
        formatar_reais(valor_ideal_esporadica),
        formatar_reais(valor_esporadica_personalizado),
        formatar_reais(total_final),
        f"{novo_percentual:.2%}".replace(".", ",")
    ]
}

resumo_df = pd.DataFrame(resumo_data)

# Estilizar a tabela com cores FRG
st.dataframe(
    resumo_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Descrição": st.column_config.Column(
            width="medium",
            help="Descrição dos itens da simulação"
        ),
        "Valor": st.column_config.Column(
            width="medium",
            help="Valores calculados na simulação"
        )
    }
)

# Botões de ação
st.markdown("""
<div style="margin-top: 2rem;">
    <div style="display: flex; gap: 1rem; justify-content: center;">
""", unsafe_allow_html=True)

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    # Botão para download da tabela
    st.download_button(
        label="📥 Baixar Relatório em Excel",
        data=converter_para_excel(resumo_df),
        file_name=f"FRG_Simulacao_Contribuicao_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
        help="Baixe um relatório completo da simulação em formato Excel"
    )

st.markdown("""
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Rodapé estilo FRG
st.markdown('<div style="margin-top: 3rem; padding: 2rem 1rem; background: linear-gradient(135deg, #8b043b 0%, #69042a 100%); color: white; border-radius: 10px; text-align: center;"><div style="margin-bottom: 1rem;"><div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">Fundação de Previdência Real Grandeza</div><div style="font-size: 0.9rem; opacity: 0.9;">Simulador de Contribuição Esporádica - Versão 2025</div></div><div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1.5rem;"><div style="text-align: center;"><div style="font-size: 0.8rem; opacity: 0.8;">Informações</div><div style="font-size: 0.9rem; font-weight: 600;">0800 888 8123</div></div><div style="text-align: center;"><div style="font-size: 0.8rem; opacity: 0.8;">Site Oficial</div><div style="font-size: 0.9rem; font-weight: 600;">www.frg.com.br</div></div></div><div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.2);"><div style="font-size: 0.8rem; opacity: 0.8;">Este simulador tem caráter informativo. Consulte o regulamento vigente para informações completas.</div></div></div>', unsafe_allow_html=True)

# Botão flutuante para nova simulação
st.markdown("""
<div style="position: fixed; bottom: 20px; right: 20px; z-index: 1000;">
""", unsafe_allow_html=True)

if st.button("🔄 Nova Simulação", key="nova_simulacao_flutuante"):
    st.rerun()

st.markdown("""
</div>
""", unsafe_allow_html=True)

# CSS adicional para melhorias finais - CORRIGIDO (cores verdes)
st.markdown("""
<style>
    /* Ajustes finais */
    .stDataFrame {
        border: 1px solid #dee2e6;
    }
    
    .stDataFrame tbody tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    
    .stDataFrame tbody tr:hover {
        background-color: #f9e9ef;  /* Corrigido: vermelho claro */
    }
    
    /* Botão flutuante */
    div[data-testid="stButton"] button[kind="secondary"] {
        background: white !important;
        color: #8b043b !important;
        border: 2px solid #8b043b !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    }
    
    div[data-testid="stButton"] button[kind="secondary"]:hover {
        background: #8b043b !important;
        color: white !important;
    }
    
    /* Ajuste de espaçamento */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
    }
    
    /* Melhorias na responsividade */
    @media (max-width: 768px) {
        .header-frg {
            padding: 1.5rem 1rem;
        }
        
        .header-frg h1 {
            font-size: 1.5rem;
        }
        
        .card-frg {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Adicionar JavaScript para melhorar a experiência
st.markdown("""
<script>
    // Rolar suavemente para as seções
    document.addEventListener('DOMContentLoaded', function() {
        // Adicionar tooltips informativos
        const inputs = document.querySelectorAll('.stNumberInput input, .stSlider input');
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.style.boxShadow = '0 0 0 3px rgba(139, 4, 59, 0.25)';  /* Corrigido: vermelho */
            });
            input.addEventListener('blur', function() {
                this.parentElement.style.boxShadow = 'none';
            });
        });
        
        // Destacar valores importantes
        const highlightValues = () => {
            const importantValues = document.querySelectorAll('[class*="valor-importante"]');
            importantValues.forEach(value => {
                value.style.animation = 'pulse 2s infinite';
            });
        };
        
        // Adicionar animação de pulso
        const style = document.createElement('style');
        style.textContent = `
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.02); }
                100% { transform: scale(1); }
            }
        `;
        document.head.appendChild(style);
    });
</script>
""", unsafe_allow_html=True)