import streamlit as st
import re
import datetime
from fpdf import FPDF

# ==========================================
# 1. BASE DE DADOS E REGRAS (EXTRAÍDAS DO EXCEL)
# ==========================================

PESOS = {
    "Estrutura": 25,
    "Cobertura": 20,
    "Acabamento Interno": 12,
    "Acabamento Externo": 12,
    "Instalações Elétricas": 7,
    "Instalações Hidráulicas": 7,
    "Pisos": 7,
    "Forro": 5,
    "Idade Real Aproximada": 5
}

OPCOES = {
    "Estrutura": {
        "Estrutura em perfeito estado (sem patologias ou necessidade de intervenção estrutural)": {"classe": "ÓTIMO", "nota": 8},
        "Estrutura íntegra (sem necessidade de reparos estruturais)": {"classe": "MUITO BOM", "nota": 7},
        "Estrutura estável (sem comprometimento estrutural)": {"classe": "BOM", "nota": 6},
        "Estrutura estável (ainda sem necessidade de intervenção estrutural)": {"classe": "INTERMEDIÁRIO", "nota": 5},
        "Estrutura sem necessidade de recuperação (sem intervenção estrutural)": {"classe": "REGULAR", "nota": 4},
        "Estabilização ou recuperação localizada do sistema estrutural (intervenção estrutural pontual)": {"classe": "DEFICIENTE", "nota": 3},
        "Estabilização ou recuperação de grande parte do sistema estrutural (comprometimento estrutural significativo)": {"classe": "RUIM", "nota": 2},
        "Estabilização ou recuperação estrutural significativa (estrutura comprometida)": {"classe": "MUITO RUIM", "nota": 1}
    },
    "Cobertura": {
        "Cobertura em bom estado (sem infiltrações ou falhas)": {"classe": "ÓTIMO", "nota": 8},
        "Cobertura em bom estado (sem necessidade de reparos)": {"classe": "MUITO BOM", "nota": 7},
        "Cobertura em condições normais (sem danos significativos)": {"classe": "BOM", "nota": 6},
        "Possível revisão da cobertura (verificação de telhas e vedação)": {"classe": "INTERMEDIÁRIO", "nota": 5},
        "Revisão necessária (possíveis reparos na impermeabilização ou telhado)": {"classe": "REGULAR", "nota": 4},
        "Revisão da impermeabilização ou substituição parcial de telhas (reparos na cobertura)": {"classe": "DEFICIENTE", "nota": 3},
        "Reparações importantes ou substituição parcial do telhado (problemas relevantes de cobertura)": {"classe": "RUIM", "nota": 2},
        "Substituição da impermeabilização ou do telhado (cobertura sem condições de uso)": {"classe": "MUITO RUIM", "nota": 1}
    },
    "Acabamento Interno": {
        "Sem fissuras ou trincas (alvenaria íntegra)/Apenas sinais de desgaste natural na pintura (manutenção estética)": {"classe": "ÓTIMO", "nota": 8},
        "Sem danos relevantes (alvenaria preservada)/Necessita apenas uma demão leve de pintura (manutenção estética simples)": {"classe": "MUITO BOM", "nota": 7},
        "Eventuais fissuras e trincas superficiais (pequenas manifestações)/Pintura interna necessária (manutenção comum)": {"classe": "BOM", "nota": 6},
        "Fissuras e trincas superficiais (desgaste natural da construção)/ Pintura necessita renovação ": {"classe": "INTERMEDIÁRIO", "nota": 5},
        "Fissuras e trincas superficiais generalizadas e alguns panos de reboco (reparos localizados)/ Pintura interna necessita de restauração do acabamento": {"classe": "REGULAR", "nota": 4},
        "Reparos em fissuras e trincas (correção de patologias na alvenaria)/ Pintura interna (recuperação estética)": {"classe": "DEFICIENTE", "nota": 3},
        "Substituição de panos de regularização da alvenaria (reconstrução parcial)/Pintura interna recuperação geral": {"classe": "RUIM", "nota": 2},
        "Alvenaria Comprometida/Pintura comprometida ou Sem pintura": {"classe": "MUITO RUIM", "nota": 1}
    },
    "Acabamento Externo": {
        "Sem fissuras ou trincas (alvenaria íntegra)/Apenas sinais de desgaste natural na pintura (manutenção estética)": {"classe": "ÓTIMO", "nota": 8},
        "Sem danos relevantes (alvenaria preservada)/Necessita apenas uma demão leve de pintura (manutenção estética simples)": {"classe": "MUITO BOM", "nota": 7},
        "Eventuais fissuras e trincas superficiais (pequenas manifestações)/Pintura interna necessária (manutenção comum)": {"classe": "BOM", "nota": 6},
        "Fissuras e trincas superficiais (desgaste natural da construção)/ Pintura necessita renovação ": {"classe": "INTERMEDIÁRIO", "nota": 5},
        "Fissuras e trincas superficiais generalizadas e alguns panos de reboco (reparos localizados)/ Pintura interna necessita de restauração do acabamento": {"classe": "REGULAR", "nota": 4},
        "Reparos em fissuras e trincas (correção de patologias na alvenaria)/ Pintura interna (recuperação estética)": {"classe": "DEFICIENTE", "nota": 3},
        "Substituição de panos de regularização da alvenaria (reconstrução parcial)/Pintura interna recuperação geral": {"classe": "RUIM", "nota": 2},
        "Pintura comprometida/Sem pintura": {"classe": "MUITO RUIM", "nota": 1}
    },
    "Instalações Elétricas": {
        "Instalações em perfeito funcionamento (sem necessidade de revisão)": {"classe": "ÓTIMO", "nota": 8},
        "Funcionamento normal (instalações operando adequadamente)": {"classe": "MUITO BOM", "nota": 7},
        "Funcionamento normal (instalações adequadas)": {"classe": "BOM", "nota": 6},
        "Eventual revisão do sistema elétrico (manutenção preventiva)": {"classe": "INTERMEDIÁRIO", "nota": 5},
        "Revisão das instalações elétricas (manutenção corretiva)": {"classe": "REGULAR", "nota": 4},
        "Revisão geral com substituição eventual de peças desgastadas (troca de componentes)": {"classe": "DEFICIENTE", "nota": 3},
        "Substituição de peças aparentes (componentes deteriorados)": {"classe": "RUIM", "nota": 2},
        "Substituição completa das instalações (sistemas deteriorados)": {"classe": "MUITO RUIM", "nota": 1}
    },
    "Instalações Hidráulicas": {
        "Instalações em perfeito funcionamento (sem necessidade de revisão)": {"classe": "ÓTIMO", "nota": 8},
        "Funcionamento normal (instalações operando adequadamente)": {"classe": "MUITO BOM", "nota": 7},
        "Funcionamento normal (instalações adequadas)": {"classe": "BOM", "nota": 6},
        "Eventual revisão do sistema hidráulico (manutenção preventiva)": {"classe": "INTERMEDIÁRIO", "nota": 5},
        "Revisão das instalações hidráulicas (manutenção corretiva)": {"classe": "REGULAR", "nota": 4},
        "Revisão geral com substituição eventual de peças desgastadas (troca de componentes)": {"classe": "DEFICIENTE", "nota": 3},
        "Substituição de peças aparentes (componentes deteriorados)": {"classe": "RUIM", "nota": 2},
        "Substituição completa das instalações (sistemas deteriorados)": {"classe": "MUITO RUIM", "nota": 1}
    },
    "Pisos": {
        "Pisos íntegros (sem desgaste relevante)": {"classe": "ÓTIMO", "nota": 8},
        "Pequeno desgaste natural (revestimentos preservados)": {"classe": "MUITO BOM", "nota": 7},
        "Pequenos reparos pontuais (desgaste localizado)": {"classe": "BOM", "nota": 6},
        "Desgaste moderado (necessidade de pequenos reparos)": {"classe": "INTERMEDIÁRIO", "nota": 5},
        "Desgaste visível em alguns ambientes (possível troca parcial)": {"classe": "REGULAR", "nota": 4},
        "Substituição pontual em alguns cômodos (revestimentos deteriorados)": {"classe": "DEFICIENTE", "nota": 3},
        "Substituição da maioria dos pisos (desgaste acentuado)": {"classe": "RUIM", "nota": 2},
        "Substituição generalizada (revestimentos comprometidos)": {"classe": "MUITO RUIM", "nota": 1}
    },
    "Forro": {
        "Forros íntegros (sem desgaste relevante)": {"classe": "ÓTIMO", "nota": 8},
        "Pequeno desgaste natural (forros preservados)": {"classe": "MUITO BOM", "nota": 7},
        "Pequenos reparos pontuais (desgaste localizado)": {"classe": "BOM", "nota": 6},
        "Desgaste moderado (necessidade de pequenos reparos)": {"classe": "INTERMEDIÁRIO", "nota": 5},
        "Desgaste visível em alguns ambientes (possível troca parcial)": {"classe": "REGULAR", "nota": 4},
        "Substituição pontual em alguns cômodos (revestimentos deteriorados)": {"classe": "DEFICIENTE", "nota": 3},
        "Substituição da maioria dos cômodos (desgaste acentuado)": {"classe": "RUIM", "nota": 2},
        "Substituição total/Sem forro": {"classe": "MUITO RUIM", "nota": 1}
    },
    "Idade Real Aproximada": {
        "até 5 anos": {"classe": "ÓTIMO", "nota": 8},
        "5 a 10 anos": {"classe": "MUITO BOM", "nota": 7},
        "10 a 20 anos": {"classe": "BOM", "nota": 6},
        "20 a 30 anos": {"classe": "INTERMEDIÁRIO", "nota": 5},
        "30 a 40 anos": {"classe": "REGULAR", "nota": 4},
        "40 a 50 anos": {"classe": "DEFICIENTE", "nota": 3},
        "50 a 60 anos": {"classe": "RUIM", "nota": 2},
        "acima de 60 anos": {"classe": "MUITO RUIM", "nota": 1}
    }
}

TABELA_FINAL = {
    8: {"classe": "ÓTIMO", "indice": 1.15,
        "texto": "Edificação nova, com até 05 anos, que apresente apenas sinais de desgaste natural na pintura externa."},
    7: {"classe": "MUITO BOM", "indice": 1.10,
        "texto": "Edificação nova ou com reforma geral e substancial que apresente apenas necessidade de uma demão leve de pintura para recompor a sua aparência."},
    6: {"classe": "BOM", "indice": 1.00,
        "texto": "Edificação seminova ou com reforma geral e substancial, cujo estado geral possa ser recuperado com reparos de eventuais fissuras e trincas superficiais, pintura externa e interna."},
    5: {"classe": "INTERMEDIÁRIO", "indice": 0.90,
        "texto": "Edificação seminova ou com reforma geral e substancial, cujo estado geral possa ser recuperado com reparos de eventuais fissuras e trincas superficiais, pintura externa e interna, eventual revisão do sistema elétrico e hidráulico."},
    4: {"classe": "REGULAR", "indice": 0.80,
        "texto": "Edificação cujo estado geral possa ser recuperado com pintura interna e externa, após reparos de fissuras e trincas superficiais generalizadas, alguns panos de reboco de alvenaria, sem recuperação do sistema estrutural, revisão do sistema elétrico e hidráulico."},
    3: {"classe": "DEFICIENTE", "indice": 0.70,
        "texto": "Edificação cujo estado geral pode ser recuperado com pintura interna e externa, após reparos de fissuras e trincas, e com estabilização e/ou recuperação localizada do sistema estrutural. As instalações hidráulicas e elétricas podem ser restauradas mediante revisão e com substituição eventual de algumas peças desgastadas naturalmente. Pode ser necessário, eventualmente, substituir os revestimentos de pisos e paredes de um cômodo ou de outro. Revisão de impermeabilização ou substituição parcial de telhas da cobertura."},
    2: {"classe": "RUIM", "indice": 0.60,
        "texto": "Edificação cujo estado geral possa ser recuperado com pintura interna e externa, com substituição de panos de regularização da alvenaria, reparos de fissuras, com estabilização e/ou recuperação de grande parte do sistema estrutura. As instalações hidráulicas e elétricas possam ser restauradas mediante a substituição das peças aparentes. A substituição dos revestimentos de pisos e paredes, da maioria dos compartimentos. Substituição ou reparações importantes na impermeabilização ou no telhado."},
    1: {"classe": "MUITO RUIM", "indice": 0.50,
        "texto": "Edificação cujo estado geral possa ser recuperado com estabilização e/ou recuperação do sistema estrutural, substituição da regularização da alvenaria, reparos de fissuras. Substituição das instalações hidráulicas e elétricas. Substituição dos revestimentos de pisos e paredes. Substituição da impermeabilização ou do telhado. "}
}

# Lista de analistas em ordem alfabética
ANALISTAS = [
    "Bruno Armoa",
    "Gisele Almeida",
    "Handrielly Ribeiro",
    "Helez Leles",
    "Leonan Brenner",
    "Luciene Ribeiro",
    "Luiz Carlos",
    "Marcio Roberto",
    "Marcos Tadeu",
    "Nadyny Insauralde",
    "Rafaela Pereira",
    "Thaylla Andressa",
    "Walber Souza"
]

# ==========================================
# 2. CONFIGURAÇÃO DA INTERFACE (UX/UI) E FUNÇÕES
# ==========================================

st.set_page_config(page_title="Classificador de Obsolescência", page_icon="🏢", layout="wide")

MENSAGEM_PADRAO = "Selecione a classificação"
MENSAGEM_ANALISTA = "Selecione o Analista..."

# Função de reset forte: Força explicitamente todos os campos a voltarem ao padrão
def limpar_dados():
    st.session_state["inscricao"] = ""
    st.session_state["analista"] = MENSAGEM_ANALISTA
    st.session_state["mostrar_resultados"] = False
    for elemento in PESOS.keys():
        st.session_state[f"sel_{elemento}"] = MENSAGEM_PADRAO

st.markdown("""
    <style>
    .big-font { font-size:20px !important; font-weight: bold; color: #1E3A8A; }
    
    .resultado-box { 
        background-color: rgba(22, 163, 74, 0.1); 
        color: var(--text-color);
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #16A34A;
    }
    
    div[data-baseweb="select"] {
        transition: all 0.3s ease;
    }
    .st-select-selecionado div[data-baseweb="select"] > div {
        background-color: rgba(34, 197, 94, 0.15) !important; 
        border-color: #22C55E !important; 
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# CABEÇALHO COM AS LOGOS
# ==========================================
st.write("") 

col_logo2, espaco_dir = st.columns([2.5, 1, 1, 2.5], vertical_alignment="center")

with col_logo2:
    st.image("logo_secretaria.png", use_container_width=True)

st.markdown("<h2 style='text-align: center;'>Assistente de Classificação do Fator de Obsolescência do Imóvel</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Selecione a descrição real do imóvel. Selecionados todos os elementos estruturais, desça a página e clique no botão <strong>CALCULAR CLASSIFICAÇÃO GERAL</strong>. O cálculo do Fob é executado automaticamente.</p>", unsafe_allow_html=True)

st.divider()

# ==========================================
# 3. IDENTIFICAÇÃO DA VISTORIA
# ==========================================
st.markdown("### 📋 Identificação do Imóvel e Analista")

# Agora usando 3 colunas para acomodar o novo campo
col_cad1, col_cad2, col_cad3 = st.columns(3)

with col_cad1:
    inscricao = st.text_input("Inscrição Cadastral do Imóvel", key="inscricao", placeholder="Ex: 01.02.003.004-5")
    if re.search(r'[A-Za-z]', inscricao):
        st.error("⚠️ A inscrição não deve conter letras. Utilize apenas números e caracteres de separação.")

with col_cad2:
    opcoes_analista = [MENSAGEM_ANALISTA] + ANALISTAS
    analista = st.selectbox("Analista Responsável", opcoes_analista, key="analista")

with col_cad3:
    data_analise = st.date_input("Data da Análise", format="DD/MM/YYYY")

st.divider()

# ==========================================
# 4. CONSTRUÇÃO DO FORMULÁRIO ESTRUTURAL
# ==========================================

selecoes = {}

col1, col2 = st.columns(2)
elementos = list(PESOS.keys())
meio = len(elementos) // 2 + 1

for i, elemento in enumerate(elementos):
    coluna_atual = col1 if i < meio else col2
    with coluna_atual:
        st.markdown(f"<span class='big-font'>{elemento} (Peso: {PESOS[elemento]}%)</span>", unsafe_allow_html=True)
        
        opcoes_texto = [MENSAGEM_PADRAO] + list(OPCOES[elemento].keys())
        
        escolha = st.selectbox(f"Selecione o estado - {elemento}", opcoes_texto, label_visibility="collapsed", key=f"sel_{elemento}")
        selecoes[elemento] = escolha
        
        if escolha != MENSAGEM_PADRAO:
            st.markdown(f'<style>div[data-testid="stSelectbox"]:has(div[id*="sel_{elemento}"]) {{ background-color: rgba(34, 197, 94, 0.15); border-radius: 0.5rem; }}</style>', unsafe_allow_html=True)
            
        st.write("") 

st.divider()

# ==========================================
# 5. BOTÕES E CÁLCULO DE RESULTADOS
# ==========================================

if "mostrar_resultados" not in st.session_state:
    st.session_state["mostrar_resultados"] = False

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    btn_calcular = st.button("CALCULAR CLASSIFICAÇÃO GERAL", type="primary", use_container_width=True)

with col_btn2:
    st.button("🔄 NOVA AVALIAÇÃO", on_click=limpar_dados, use_container_width=True)

if btn_calcular:
    itens_pendentes = [item for item, desc in selecoes.items() if desc == MENSAGEM_PADRAO]
    
    # Validações de Segurança atualizadas
    if not inscricao.strip():
        st.error("⚠️ Atenção! Você esqueceu de preencher a Inscrição Cadastral.")
        st.session_state["mostrar_resultados"] = False
    elif re.search(r'[A-Za-z]', inscricao):
        st.error("⚠️ Atenção! Corrija a Inscrição Cadastral (letras não são permitidas).")
        st.session_state["mostrar_resultados"] = False
    elif analista == MENSAGEM_ANALISTA:
        st.error("⚠️ Atenção! Você esqueceu de selecionar o Analista Responsável.")
        st.session_state["mostrar_resultados"] = False
    elif itens_pendentes:
        st.error(f"⚠️ Atenção! Você esqueceu de preencher os seguintes itens: **{', '.join(itens_pendentes)}**.")
        st.session_state["mostrar_resultados"] = False
    else:
        st.session_state["mostrar_resultados"] = True

# Se tudo estiver correto, exibe os resultados e gera o PDF
if st.session_state["mostrar_resultados"]:
    soma_pesos = 0
    soma_contribuicoes = 0

    for elemento, descricao in selecoes.items():
        peso = PESOS[elemento]
        dados_opcao = OPCOES[elemento][descricao]
        nota = dados_opcao["nota"]

        contribuicao = nota * peso
        soma_pesos += peso
        soma_contribuicoes += contribuicao

    nota_final = soma_contribuicoes / soma_pesos if soma_pesos > 0 else 0
    nota_arredondada = int(round(nota_final))
    nota_arredondada = max(1, min(8, nota_arredondada))

    resultado_final = TABELA_FINAL[nota_arredondada]

    st.subheader("📊 Resultados Matemáticos")
    res_c1, res_c2, res_c3 = st.columns(3)
    res_c1.metric(label="Soma Pesos Utilizados", value=f"{soma_pesos}%")
    res_c2.metric(label="Soma Contribuições", value=f"{soma_contribuicoes}")
    res_c3.metric(label="Nota Final (Média)", value=f"{nota_final:.2f}")

    st.markdown("---")

    st.markdown("### Enquadramento do Fator de Obsolescência de Acordo com o Decreto Nº 11.665 de 30 de Dezembro de 2025")
    st.markdown(f"""
        <div class="resultado-box">
            <h2>Classificação: {resultado_final['classe']}</h2>
            <h4>Índice Fob: {resultado_final['indice']}</h4>
            <p><strong>Descrição Legal:</strong> {resultado_final['texto']}</p>
        </div>
    """, unsafe_allow_html=True)

    # ==========================================
    # GERADOR DE RELATÓRIO PDF (OTIMIZADO PARA 1 PÁGINA)
    # ==========================================
    def gerar_pdf_bytes():
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.set_margins(15, 10, 15)
        pdf.add_page()
        
        def limpa_txt(texto):
            return str(texto).encode('latin-1', 'replace').decode('latin-1')

        # Inserindo as Logos Centralizadas
       
        try:
            pdf.image("logo_secretaria.png", x=110, y=10, w=35)
        except: pass

        pdf.set_y(28) 

        # Título
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 8, limpa_txt("Relatório de Classificação - Fator de Obsolescência"), ln=1, align="C")
        pdf.ln(4)

        # Dados Básicos (Inscrição, Analista e Data)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, limpa_txt(f"Inscrição Cadastral: {inscricao}"), ln=1)
        pdf.cell(0, 6, limpa_txt(f"Analista Responsável: {analista}"), ln=1)
        pdf.cell(0, 6, limpa_txt(f"Data da Análise: {data_analise.strftime('%d/%m/%Y')}"), ln=1)
        pdf.ln(3)

        # Opções Estruturais Selecionadas
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 7, limpa_txt("Itens Estruturais Avaliados:"), fill=True, ln=1)
        pdf.ln(2)
        
        for k, v in selecoes.items():
            pdf.set_font("Arial", "B", 9)
            pdf.cell(0, 5, limpa_txt(f"{k}:"), ln=1)
            pdf.set_font("Arial", "", 9)
            pdf.multi_cell(0, 5, limpa_txt(str(v)))
            pdf.ln(1)

        # Resultados Matemáticos
        pdf.ln(2)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 7, limpa_txt("Resultados Matemáticos:"), fill=True, ln=1)
        pdf.ln(2)
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 5, limpa_txt(f"Soma Pesos Utilizados: {soma_pesos}%"), ln=1)
        pdf.cell(0, 5, limpa_txt(f"Soma Contribuições: {soma_contribuicoes}"), ln=1)
        pdf.cell(0, 5, limpa_txt(f"Nota Final (Média): {nota_final:.2f}"), ln=1)

        # Caixa do Resultado Final (Verde)
        pdf.ln(3)
        pdf.set_fill_color(230, 245, 230)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, limpa_txt(f"Classificação Oficial: {resultado_final['classe']}"), fill=True, align="C", ln=1)
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 8, limpa_txt(f"Índice Fob: {resultado_final['indice']}"), fill=True, align="C", ln=1)
        pdf.set_font("Arial", "I", 10)
        pdf.multi_cell(0, 6, limpa_txt(f"Descrição Legal: {resultado_final['texto']}"), fill=True)

        pdf_bytes = pdf.output()
        return bytes(pdf_bytes)

    # Botão de Download
    st.markdown("---")
    st.markdown("### 📥 Documento Oficial")
    
    st.download_button(
        label="📄 BAIXAR RELATÓRIO EM PDF",
        data=gerar_pdf_bytes(),
        file_name=f"Relatorio_Vistoria_{inscricao}.pdf",
        mime="application/pdf",
        type="primary",
        use_container_width=True
    )
