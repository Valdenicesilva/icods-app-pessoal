import streamlit as st
import datetime

# Configuração da Página
st.set_page_config(
    page_title="ICODS - Trilha de Desenvolvimento & Behavioral Compliance",
    page_icon="⚖️",
    layout="wide"
)

# Inicialização do Session State
def init_session_state():
    defaults = {
        'fase_atual': 1,
        'nome': '',
        'formacao': '',
        'experiencia': '',
        'contexto_regiao': '',
        'interesses': [],
        'ambiente_ideal': '',
        'raca_etnia': 'Selecione...',
        'faixa_renda': 'Selecione...',
        'dilema_resposta': '',
        'reflexao_fase2': '',
        'reflexao_fase3': '',
        'reflexao_fase4': '',
        'fase1_ok': False,
        'fase2_ok': False,
        'fase3_ok': False,
        'fase4_ok': False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session_state()

# Estilização CSS Personalizada
st.markdown("""
    <style>
    .main-header { font-size: 26px; font-weight: 700; color: #1E3A8A; margin-bottom: 10px; }
    .sub-header { font-size: 18px; font-weight: 600; color: #374151; margin-bottom: 15px; }
    .card { background-color: #F8FAFC; padding: 20px; border-radius: 10px; border: 1px solid #E2E8F0; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# Sidebar / Menu de Navegação Gated
st.sidebar.markdown("# 🧭 Trilha ICODS")
st.sidebar.markdown("---")

fase_labels = {
    1: "Fase 1: Diagnóstico Comportamental",
    2: "Fase 2: Inteligência de Mercado Regional",
    3: "Fase 3: Ecossistemas de Trabalho",
    4: "Fase 4: Upskilling & Currículo Humanizado",
    5: "Fase 5: Banco de Talentos & Relatório"
}

# Lógica de liberação de fases (Gated Navigation)
def pode_acessar(fase):
    if fase == 1: return True
    if fase == 2: return st.session_state.get('fase1_ok', False)
    if fase == 3: return st.session_state.get('fase2_ok', False)
    if fase == 4: return st.session_state.get('fase3_ok', False)
    if fase == 5: return st.session_state.get('fase4_ok', False)
    return False

selected_fase = st.sidebar.radio("Selecione a Etapa:", [1, 2, 3, 4, 5], format_func=lambda x: fase_labels[x])

if selected_fase > st.session_state.fase_atual and not pode_acessar(selected_fase):
    st.sidebar.warning("⚠️ Conclua a etapa anterior e salve as notas de progresso para avançar!")
    selected_fase = st.session_state.fase_atual

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reiniciar Processo"):
    st.session_state.clear()
    st.rerun()

# --- FASE 1: DIAGNÓSTICO COMPORTAMENTAL ---
if selected_fase == 1:
    st.markdown('<div class="main-header">Fase 1: Diagnóstico Comportamental & Alinhamento Ético</div>', unsafe_allow_html=True)
    st.markdown("Mapeamento inicial de perfil, aspirações, critérios demográficos e tomada de decisão fundamentada em Behavioral Compliance.")
    
    with st.form("form_fase1"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome Completo (*Obrigatório)", value=st.session_state.get('nome', ''))
            formacao = st.text_input("Formação Acadêmica (*Obrigatório)", value=st.session_state.get('formacao', ''))
            
            opcoes_raca = ["Selecione...", "Branca", "Preta", "Parda", "Amarela", "Indígena", "Prefiro não declarar"]
            raca_atual = st.session_state.get('raca_etnia', 'Selecione...')
            idx_raca = opcoes_raca.index(raca_atual) if raca_atual in opcoes_raca else 0
            raca_etnia = st.selectbox("Raça / Etnia (*Obrigatório)", opcoes_raca, index=idx_raca)
            
            interesses = st.multiselect(
                "Áreas de Interesse Profissional",
                ["Compliance", "Direito", "RH", "Gestão", "Tecnologia", "Operações", "Educação Corporativa", "Políticas Públicas"],
                default=st.session_state.get('interesses', [])
            )
        with col2:
            experiencia = st.text_input("Área de Experiência Principal (*Obrigatório)", value=st.session_state.get('experiencia', ''))
            contexto_regiao = st.text_input("Cidade e Estado onde Reside (*Obrigatório)", value=st.session_state.get('contexto_regiao', ''))
            
            opcoes_renda = ["Selecione...", "Sem renda / Desempregado(a)", "Até 1 salário mínimo", "De 1 a 3 salários mínimos", "De 3 a 5 salários mínimos", "Acima de 5 salários mínimos", "Prefiro não declarar"]
            renda_atual = st.session_state.get('faixa_renda', 'Selecione...')
            idx_renda = opcoes_renda.index(renda_atual) if renda_atual in opcoes_renda else 0
            faixa_renda = st.selectbox("Faixa de Renda Atual (*Obrigatório)", opcoes_renda, index=idx_renda)
            
            ambiente_ideal = st.text_input("Ambiente Corporativo Desejado (*Obrigatório)", value=st.session_state.get('ambiente_ideal', ''))

        st.markdown("---")
        st.markdown("### Resolução Guiada de Dilema Comportamental")
        st.info("Dilema: Você identifica uma falha em um processo interno que pode gerar passivo regulatório, mas a liderança imediata prefere não reportar para evitar atritos. Qual sua conduta sob a ótica do Behavioral Compliance?")
        dilema_resposta = st.text_area("Descreva sua linha de ação fundamentada:", value=st.session_state.get('dilema_resposta', ''))

        submitted_f1 = st.form_submit_button("Salvar e Avançar para Fase 2 ➡️")
        if submitted_f1:
            if not nome or not formacao or not experiencia or not contexto_regiao or not ambiente_ideal or raca_etnia == "Selecione..." or faixa_renda == "Selecione..." or not dilema_resposta:
                st.error("❌ Por favor, preencha todos os campos obrigatórios, selecione raça/etnia, faixa de renda e responda ao dilema.")
            else:
                st.session_state['nome'] = nome
                st.session_state['formacao'] = formacao
                st.session_state['raca_etnia'] = raca_etnia
                st.session_state['interesses'] = interesses
                st.session_state['experiencia'] = experiencia
                st.session_state['contexto_regiao'] = contexto_regiao
                st.session_state['faixa_renda'] = faixa_renda
                st.session_state['ambiente_ideal'] = ambiente_ideal
                st.session_state['dilema_resposta'] = dilema_resposta
                st.session_state['fase1_ok'] = True
                st.session_state.fase_atual = 2
                st.success("✅ Fase 1 concluída com sucesso! Redirecionando...")
                st.rerun()

# --- FASE 2: INTELIGÊNCIA DE MERCADO REGIONAL ---
elif selected_fase == 2:
    st.markdown('<div class="main-header">Fase 2: Inteligência de Mercado & Raio-X Regional</div>', unsafe_allow_html=True)
    st.markdown(f"Análise de empregabilidade cruzando o perfil de **{st.session_state.get('contexto_regiao')}** com demandas setoriais e diversidade demográfica.")
    
    with st.container(border=True):
        st.markdown("### 📊 Indicadores e Oportunidades Setoriais")
        st.write("Com base no seu escopo de atuação e região, observe o alinhamento entre as demandas locais e as diretrizes de compliance e governança.")
        st.markdown("- **Setores em destaque:** Indústria, Serviços Especializados, Educação Corporativa e Gestão Pública.")
        st.markdown("- **Diretriz de Compliance:** Organizações buscam profissionais capazes de unir eficiência operacional com integridade e conformidade regulatória.")

    with st.form("form_fase2"):
        st.markdown("### 📝 Notas de Progresso e Síntese Regional")
        st.write("Registre seus insights sobre as oportunidades locais e lacunas identificadas em sua região:")
        reflexao_fase2 = st.text_area("Notas de Progresso (Fase 2):", value=st.session_state.get('reflexao_fase2', ''))
        
        submitted_f2 = st.form_submit_button("Salvar e Avançar para Fase 3 ➡️")
        if submitted_f2:
            if not reflexao_fase2.strip():
                st.error("❌ Por favor, preencha suas notas de progresso para avançar.")
            else:
                st.session_state['reflexao_fase2'] = reflexao_fase2
                st.session_state['fase2_ok'] = True
                st.session_state.fase_atual = 3
                st.success("✅ Fase 2 salva com sucesso!")
                st.rerun()

# --- FASE 3: ECOSSISTEMAS DE TRABALHO ---
elif selected_fase == 3:
    st.markdown('<div class="main-header">Fase 3: Ecossistemas de Trabalho (Remoto, Híbrido e Presencial)</div>', unsafe_allow_html=True)
    st.markdown("Autoavaliação de prontidão para diferentes modelos organizacionais e gestão de autonomia profissional.")
    
    with st.container(border=True):
        st.markdown("### ⚖️ Matriz de Prontidão Operacional")
        st.write("Avalie seu perfil frente às exigências de autogestão, comunicação assíncrona e segurança de dados nos regimes remotos e híbridos.")

    with st.form("form_fase3"):
        st.markdown("### 📝 Notas de Progresso e Estratégia de Adaptação")
        reflexao_fase3 = st.text_area("Descreva sua estratégia para o modelo de trabalho escolhido:", value=st.session_state.get('reflexao_fase3', ''))
        
        submitted_f3 = st.form_submit_button("Salvar e Avançar para Fase 4 ➡️")
        if submitted_f3:
            if not reflexao_fase3.strip():
                st.error("❌ Por favor, preencha suas notas de progresso para avançar.")
            else:
                st.session_state['reflexao_fase3'] = reflexao_fase3
                st.session_state['fase3_ok'] = True
                st.session_state.fase_atual = 4
                st.success("✅ Fase 3 salva com sucesso!")
                st.rerun()

# --- FASE 4: UPSKILLING E CURRÍCULO HUMANIZADO ---
elif selected_fase == 4:
    st.markdown('<div class="main-header">Fase 4: Upskilling, Currículo Humanizado & Apoio</div>', unsafe_allow_html=True)
    st.markdown("Diretrizes para construção de currículos enxutos focados em entregas e alinhados a sistemas ATS, além de suporte contínuo.")

    with st.container(border=True):
        st.markdown("### 📄 Diretrizes de Currículo Baseado em Entregas")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**O que incluir:**")
            st.markdown("- Resultados quantificáveis e projetos de compliance implantados.")
            st.markdown("- Palavras-chave alinhadas à sua área de especialização.")
        with col_b:
            st.markdown("**O que evitar:**")
            st.markdown("- Excesso de páginas ou informações genéricas.")
            st.markdown("- Descrições puramente de tarefas sem impacto mensurável.")

    with st.form("form_fase4"):
        st.markdown("### 📝 Notas de Progresso e Plano de Upskilling")
        reflexao_fase4 = st.text_area("Descreva as competências que irá aprimorar e as diretrizes do seu currículo:", value=st.session_state.get('reflexao_fase4', ''))
        
        submitted_f4 = st.form_submit_button("Salvar e Concluir Trilha ➡️")
        if submitted_f4:
            if not reflexao_fase4.strip():
                st.error("❌ Por favor, preencha suas notas de progresso para concluir a trilha.")
            else:
                st.session_state['reflexao_fase4'] = reflexao_fase4
                st.session_state['fase4_ok'] = True
                st.session_state.fase_atual = 5
                st.success("✅ Trilha concluída com sucesso! Acesse o Relatório Final.")
                st.rerun()

# --- FASE 5: BANCO DE TALENTOS & RELATÓRIO FINAL ---
elif selected_fase == 5:
    st.markdown('<div class="main-header">Fase 5: Banco de Talentos ICODS & Relatório Final</div>', unsafe_allow_html=True)
    st.markdown("Consolidação da jornada, visualização do perfil e geração do relatório de desenvolvimento descarregável.")

    interesses_str = ", ".join(st.session_state.get('interesses', []))

    with st.container(border=True):
        st.markdown(f"### 👤 Perfil Consolidado: {st.session_state.get('nome')}")
        st.markdown(f"**Formação:** {st.session_state.get('formacao')} | **Experiência:** {st.session_state.get('experiencia')}")
        st.markdown(f"**Raça/Etnia:** {st.session_state.get('raca_etnia')} | **Faixa de Renda:** {st.session_state.get('faixa_renda')}")
        st.markdown(f"**Localidade:** {st.session_state.get('contexto_regiao')} | **Áreas de Interesse:** {interesses_str}")
        st.markdown(f"**Ambiente Desejado:** {st.session_state.get('ambiente_ideal')}")

    st.markdown("---")
    st.markdown("### 📥 Relatório Final de Desenvolvimento (Download)")
    st.write("O relatório abaixo consolida seus dados cadastrais, respostas aos dilemas éticos e notas de progresso de cada fase.")

    relatorio_texto = f"""==================================================
RELATÓRIO FINAL DE DESENVOLVIMENTO - PLATAFORMA ICODS
Behavioral Compliance & Orientação Profissional
==================================================
Data de Geração: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}

1. DADOS CADASTRAIS E PERFIL DEMOGRÁFICO
- Nome: {st.session_state.get('nome')}
- Formação: {st.session_state.get('formacao')}
- Raça/Etnia: {st.session_state.get('raca_etnia')}
- Faixa de Renda: {st.session_state.get('faixa_renda')}
- Experiência Principal: {st.session_state.get('experiencia')}
- Região: {st.session_state.get('contexto_regiao')}
- Áreas de Interesse: {interesses_str}
- Ambiente Ideal: {st.session_state.get('ambiente_ideal')}

2. RESOLUÇÃO DE DILEMA ÉTICO (FASE 1)
{st.session_state.get('dilema_resposta')}

3. NOTAS DE PROGRESSO - INTELIGÊNCIA DE MERCADO (FASE 2)
{st.session_state.get('reflexao_fase2')}

4. NOTAS DE PROGRESSO - ECOSSISTEMAS DE TRABALHO (FASE 3)
{st.session_state.get('reflexao_fase3')}

5. NOTAS DE PROGRESSO - UPSKILLING E CURRÍCULO (FASE 4)
{st.session_state.get('reflexao_fase4')}

==================================================
Plataforma ICODS - Governança e Transparência
==================================================
"""

    st.download_button(
        label="📥 Baixar Relatório Final (.txt)",
        data=relatorio_texto,
        file_name=f"Relatorio_ICODS_{st.session_state.get('nome', 'Profissional').replace(' ', '_')}.txt",
        mime="text/plain"
    )
