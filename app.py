import streamlit as st
from PIL import Image
import os
import textwrap
from supabase import create_client

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Plataforma ICODS - Trilha de Desenvolvimento e Oportunidades", layout="wide")

# --- CONEXÃO COM O SUPABASE ---
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()

# --- INICIALIZAÇÃO DO SESSION STATE ---
paginas_validas = ['Inicio', 'Diagnostico', 'Fase2', 'Fase3', 'Fase4', 'Fase5', 'Relatorio']
if 'pagina_atual' not in st.session_state or st.session_state['pagina_atual'] not in paginas_validas:
    st.session_state['pagina_atual'] = 'Inicio'

# Inicialização dos dados do usuário (Fases e Navegação)
if 'nome' not in st.session_state: st.session_state['nome'] = ''
if 'formacao' not in st.session_state: st.session_state['formacao'] = ''
if 'experiencia' not in st.session_state: st.session_state['experiencia'] = ''
if 'interesses' not in st.session_state: st.session_state['interesses'] = []
if 'contexto_regiao' not in st.session_state: st.session_state['contexto_regiao'] = ''
if 'ambiente_ideal' not in st.session_state: st.session_state['ambiente_ideal'] = ''
if 'cenario_simulado' not in st.session_state: st.session_state['cenario_simulado'] = 0
if 'questao_etica' not in st.session_state: st.session_state['questao_etica'] = ''

# Variáveis para armazenar os resultados e notas das fases
if 'resultado_fase2' not in st.session_state: st.session_state['resultado_fase2'] = ''
if 'resultado_fase3' not in st.session_state: st.session_state['resultado_fase3'] = ''
if 'resultado_fase4' not in st.session_state: st.session_state['resultado_fase4'] = ''
if 'resultado_fase5' not in st.session_state: st.session_state['resultado_fase5'] = ''
if 'optin_banco_talentos' not in st.session_state: st.session_state['optin_banco_talentos'] = False

# Travas de conclusão de fases (Validação Comportamental de Fluxo)
if 'fase1_concluida' not in st.session_state: st.session_state['fase1_concluida'] = False
if 'fase2_concluida' not in st.session_state: st.session_state['fase2_concluida'] = False
if 'fase3_concluida' not in st.session_state: st.session_state['fase3_concluida'] = False
if 'fase4_concluida' not in st.session_state: st.session_state['fase4_concluida'] = False
if 'fase5_concluida' not in st.session_state: st.session_state['fase5_concluida'] = False

# --- FUNÇÃO PARA CARREGAR IMAGENS COM SEGURANÇA ---
def carregar_imagem(nome_arquivo):
    """Carrega uma imagem da pasta local (raiz)."""
    try:
        diretorio_atual = os.getcwd()
        caminho_completo = os.path.join(diretorio_atual, nome_arquivo)

        if os.path.exists(caminho_completo):
            return Image.open(caminho_completo)
        else:
            return None
    except Exception as e:
        return None

# --- DEFINIÇÃO DAS PÁGINAS (FUNÇÕES) ---
def pagina_inicio():
    st.title("Trilha de Orientação Profissional e Behavioral Compliance")
    st.markdown("---")
    img_inicio = carregar_imagem("fot_fundo.jpg")
    if img_inicio:
        st.image(img_inicio, caption="ICODS - Desenvolvimento Comportamental", width=400)
    st.markdown("""
    ### Bem-vindo(a) à sua jornada de desenvolvimento profissional.
    Esta plataforma foi desenhada para apoiar a sua transição de carreira e empregabilidade,
    aliando o seu perfil comportamental a práticas éticas de compliance, upskilling, suporte psicológico e conexões de alto valor.

    Utilize os botões abaixo para navegar entre as fases do programa.
    """)
    st.markdown("---")
    if st.button("Iniciar Diagnóstico", key='btn_inicio_diag', type="primary"):
        st.session_state['pagina_atual'] = 'Diagnostico'
        st.rerun()

def pagina_diagnostico():
    st.header("Fase 1: Diagnóstico Comportamental e de Carreira")
    st.markdown("---")
    
    st.subheader("📌 Camada 1: Aspirações, Contexto e Alinhamento de Valores")
    st.write("Mapeie suas preferências profissionais, áreas de interesse e o cenário contextual em que você atua.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Nome Completo (*Obrigatório)", key='nome')
        st.text_input("Formação Acadêmica (*Obrigatório)", key='formacao')
        st.multiselect("Áreas de Interesse Profissional", ["Compliance", "Direito", "RH", "Gestão", "Tecnologia", "Operações"], key='interesses')
    with col2:
        st.text_input("Área de Experiência Principal (*Obrigatório)", key='experiencia')
        st.text_input("Cidade e Estado onde Reside (*Obrigatório)", key='contexto_regiao')
        st.text_input("Ambiente Corporativo Ideal (*Obrigatório)", key='ambiente_ideal')

    st.markdown("---")
    
    st.subheader("⚙️ Camada 2: Cenários Simulados de Tomada de Decisão (O Comportamento em Ação)")
    st.write("Analise o mini-dilema prático abaixo e escolha a conduta que melhor reflete sua postura profissional diante de desafios reais:")

    with st.container(border=True):
        st.markdown("**Desafio Prático:** *Você está sob um prazo extremamente apertado para entregar um relatório crítico de conformidade, mas percebe uma inconsistência de dados que pode invalidar parte da conclusão. O que você faz?*")
        st.radio(
            "Selecione a conduta que melhor descreve sua abordagem:",
            [
                "A) Entrego o relatório no prazo com a inconsistência e aviso a liderança depois para evitar atrasos.",
                "B) Alerto imediatamente a liderança sobre a inconsistência, proponho um ajuste rápido e renegocio o prazo se necessário.",
                "C) Paro a entrega totalmente e refaço todo o processo sozinho, sem comunicar o impacto no prazo imediato.",
                "D) Ignoro a inconsistência, pois o volume de entregas anterior compensa o erro pontual."
            ],
            key='cenario_simulado'
        )

    st.markdown("---")
    st.text_area("Descreva brevemente sua reflexão sobre o cenário ou um dilema ético real que já enfrentou (Opcional)", key='questao_etica')
    st.markdown("---")

    col_bt1, col_bt2, col_bt3 = st.columns([1, 1, 4])
    with col_bt1:
         if st.button("Voltar ao Início", key='btn_diag_voltar'):
            st.session_state['pagina_atual'] = 'Inicio'
            st.rerun()
    with col_bt3:
        if st.button("Avançar para Fase 2: Raio-X e Oportunidades", key='btn_diag_avancar', type="primary"):
            if not st.session_state.get('nome') or not st.session_state.get('formacao') or not st.session_state.get('experiencia') or not st.session_state.get('contexto_regiao') or not st.session_state.get('ambiente_ideal'):
                st.warning("⚠️ **Atenção:** Preencha todos os campos obrigatórios (Nome, Formação, Experiência, Contexto Regional e Ambiente Ideal) para prosseguir na trilha.")
            else:
                st.session_state['fase1_concluida'] = True
                st.session_state['pagina_atual'] = 'Fase2'
                st.rerun()

def pagina_fase2():
    if not st.session_state.get('fase1_concluida'):
        st.warning("🔒 **Acesso Bloqueado:** Você precisa concluir a Fase 1 (Diagnóstico) preenchendo todos os campos obrigatórios antes de acessar esta etapa.")
        if st.button("Ir para Fase 1 (Diagnóstico)"):
            st.session_state['pagina_atual'] = 'Diagnostico'
            st.rerun()
        return

    st.header("Fase 2: Inteligência de Mercado e Oportunidades Locais")
    st.markdown("---")

    st.markdown("### 📊 Raio-X do Mercado por Região")
    st.write("Selecione a região, o estado e o município desejado para consultar os indicadores oficiais de empregabilidade.")

    try:
        response_all = supabase.table("indicadores_regionais").select("regiao, estado, cidade").execute()
        dados_db = response_all.data if response_all.data else []
    except Exception as e:
        dados_db = []
        st.error(f"Erro ao carregar dados do Supabase: {e}")

    if not dados_db:
        st.warning("⚠️ Nenhum indicador regional encontrado no banco de dados. Insira dados na tabela `indicadores_regionais` para iniciar.")
    else:
        regioes_disponiveis = sorted(list(set(item["regiao"] for item in dados_db if item.get("regiao"))))
        regiao_selecionada = st.selectbox("Selecione a Região:", regioes_disponiveis)

        estados_disponiveis = sorted(list(set(item["estado"] for item in dados_db if item.get("regiao") == regiao_selecionada and item.get("estado"))))
        
        if estados_disponiveis:
            estado_selecionado = st.selectbox("Selecione o Estado:", estados_disponiveis)

            cidades_disponiveis = sorted(list(set(item["cidade"] for item in dados_db if item.get("estado") == estado_selecionado and item.get("cidade"))))
            
            if cidades_disponiveis:
                cidade_selecionada = st.selectbox("Selecione o Município:", cidades_disponiveis)
                
                response = supabase.table("indicadores_regionais").select("*").eq("cidade", cidade_selecionada).execute()
                dados = response.data[0] if response.data else None

                if dados:
                    st.info(f"📅 **Mês de Referência dos Dados:** {dados.get('mes_referencia', 'N/A')}")
                    faixa = dados.get('faixa_etaria', 'Sem dados cadastrados.')
                    genero = dados.get('genero_raca', 'Sem dados cadastrados.')
                    setores = dados.get('setores_lideres', [])

                    st.markdown("---")
                    col_card1, col_card2 = st.columns(2)
                    
                    with col_card1:
                        with st.container(border=True):
                            st.markdown(f"### 📈 Perfil de Contratações")
                            st.markdown(f"**Município:** {cidade_selecionada}")
                            st.markdown(f"**Destaque por Faixa Etária:** {faixa}")
                            st.markdown(f"**Recorte de Gênero/Raça:** {genero}")
                            
                    with col_card2:
                        with st.container(border=True):
                            st.markdown(f"### 🏭 Setores que Mais Empregam")
                            if setores:
                                for idx, setor in enumerate(setores, 1):
                                    st.markdown(f"{idx}. **{setor}**")
                            else:
                                st.markdown("Nenhum setor registrado.")

                    st.success("💡 **Dica de Direcionamento Profissional:** O app cruza o seu perfil comportamental com a realidade econômica deste município.")

    st.markdown("---")
    st.write("### Notas e Alinhamento Profissional (*Obrigatório preencher para avançar*)")
    st.text_area("Notas de progresso na Fase 2", key='resultado_fase2', height=150, placeholder="Escreva suas reflexões sobre as oportunidades mapeadas...")

    st.markdown("---")
    col_bt1, col_bt2, col_bt3 = st.columns([1, 1, 4])
    with col_bt1:
         if st.button("Voltar ao Diagnóstico", key='btn_f2_voltar'):
            st.session_state['pagina_atual'] = 'Diagnostico'
            st.rerun()
    with col_bt3:
        if st.button("Avançar para Fase 3: Trabalho Remoto", key='btn_f2_avancar', type="primary"):
            if not st.session_state.get('resultado_fase2'):
                st.warning("⚠️ **Atenção:** Escreva suas notas de reflexão na Fase 2 antes de prosseguir para a próxima etapa.")
            else:
                st.session_state['fase2_concluida'] = True
                st.session_state['pagina_atual'] = 'Fase3'
                st.rerun()

def pagina_fase3():
    if not st.session_state.get('fase2_concluida'):
        st.warning("🔒 **Acesso Bloqueado:** Conclua e salve as notas da Fase 2 antes de acessar esta etapa.")
        if st.button("Ir para Fase 2"):
            st.session_state['pagina_atual'] = 'Fase2'
            st.rerun()
        return

    st.header("Fase 3: O Ecossistema Virtual e de Trabalho Remoto")
    st.markdown("---")
    
    st.markdown("### 🌐 Rompendo Barreiras Geográficas")
    st.write("Esta fase expande suas oportunidades para além do mercado local, conectando você a vagas de trabalho remoto.")

    st.markdown("#### 🔍 Avaliação de Prontidão para o Trabalho Remoto")
    with st.container(border=True):
        col_f3_1, col_f3_2 = st.columns(2)
        with col_f3_1:
            st.markdown("**Infraestrutura Tecnológica**")
            internet = st.checkbox("Possuo internet banda larga estável", key="rem_internet")
            computador = st.checkbox("Computador/Notebook em bom estado", key="rem_pc")
            espaco = st.checkbox("Espaço físico adequado e silencioso", key="rem_espaco")
        with col_f3_2:
            st.markdown("**Perfil Comportamental e Autonomia**")
            autonomia = st.checkbox("Facilidade para gerenciar próprio tempo e prazos", key="rem_autonomia")
            comunicacao = st.checkbox("Boa comunicação escrita e digital", key="rem_comunicacao")
            aprendizado = st.checkbox("Disposição para aprendizado contínuo", key="rem_aprendizado")

        itens_checados = sum([internet, computador, espaco, autonomia, comunicacao, aprendizado])
        st.markdown("---")
        if itens_checados == 6:
            st.success("🌟 **Prontidão Excelente!** Requisitos ideais para atuar em regime remoto.")
        elif itens_checados >= 4:
            st.info("👍 **Boa Prontidão!** Base sólida, atente-se apenas aos itens pendentes.")
        else:
            st.warning("⚠️ **Atenção aos Requisitos:** O trabalho remoto exige forte autonomia.")

    st.markdown("---")
    st.markdown("### 💼 Portais de Trabalho Remoto")
    col_plat1, col_plat2, col_plat3 = st.columns(3)
    with col_plat1:
        with st.container(border=True):
            st.markdown("#### 🚀 Remotar & Coodesh")
            st.markdown("[🔗 Acessar Remotar](https://remotar.com.br/)")
            st.markdown("[🔗 Acessar Coodesh](https://coodesh.com/)")
    with col_plat2:
        with st.container(border=True):
            st.markdown("#### 💻 Tech & Digital")
            st.markdown("[🔗 Geek Hunter](https://www.geekhunter.com.br/)")
            st.markdown("[🔗 Trampos.co](https://trampos.co/)")
    with col_plat3:
        with st.container(border=True):
            st.markdown("#### 🌍 Global")
            st.markdown("[🔗 We Work Remotely](https://weworkremotely.com/)")
            st.markdown("[🔗 Remote.co](https://remote.co/)")

    st.markdown("---")
    st.text_area("Notas de progresso na Fase 3 (*Obrigatório preencher para avançar*)", key='resultado_fase3', height=150)

    st.markdown("---")
    col_bt1, col_bt2, col_bt3 = st.columns([1, 1, 4])
    with col_bt1:
         if st.button("Voltar à Fase 2", key='btn_f3_voltar'):
            st.session_state['pagina_atual'] = 'Fase2'
            st.rerun()
    with col_bt3:
        if st.button("Avançar para Fase 4: Trabalho Presencial e Híbrido", key='btn_f3_avancar', type="primary"):
            if not st.session_state.get('resultado_fase3'):
                st.warning("⚠️ **Atenção:** Preencha as notas de progresso da Fase 3 para prosseguir.")
            else:
                st.session_state['fase3_concluida'] = True
                st.session_state['pagina_atual'] = 'Fase4'
                st.rerun()

def pagina_fase4():
    if not st.session_state.get('fase3_concluida'):
        st.warning("🔒 **Acesso Bloqueado:** Conclua a Fase 3 preenchendo as notas de progresso antes de acessar esta etapa.")
        if st.button("Ir para Fase 3"):
            st.session_state['pagina_atual'] = 'Fase3'
            st.rerun()
        return

    st.header("Fase 4: O Ecossistema Presencial, Híbrido e Compliance Físico")
    st.markdown("---")
    
    st.markdown("### 🏛️ Dinâmicas do Trabalho Presencial e Rituais Corporativos")
    st.write("Esta fase avalia sua adaptação aos modelos presenciais e híbridos e às interações de *behavioral compliance* no ambiente físico.")

    with st.container(border=True):
        col_f4_1, col_f4_2 = st.columns(2)
        with col_f4_1:
            st.markdown("**Infraestrutura Física e Logística**")
            deslocamento = st.checkbox("Lido bem com o tempo de deslocamento (*commute*)", key="pres_deslocamento")
            rituais = st.checkbox("Valorizo rituais corporativos físicos e reuniões face a face", key="pres_rituais")
            seguranca_fisica = st.checkbox("Cuido rigorosamente de sigilo documental e segurança na mesa", key="pres_seguranca")
        with col_f4_2:
            st.markdown("**Relações Interpessoais e Hierarquia**")
            hierarquia = st.checkbox("Adaptação a estruturas hierárquicas tradicionais", key="pres_hierarquia")
            comunicacao_direta = st.checkbox("Prefiro a agilidade da comunicação direta no escritório", key="pres_comunicacao")
            colaboracao = st.checkbox("Gosto de dinâmicas colaborativas e brainstorms presenciais", key="pres_colaboracao")

        itens_presenciais = sum([deslocamento, rituais, seguranca_fisica, hierarquia, comunicacao_direta, colaboracao])
        st.markdown("---")
        if itens_presenciais == 6:
            st.success("🌟 **Fit Presencial Excelente!** Forte sinergia com escritórios e rituais tradicionais.")
        elif itens_presenciais >= 4:
            st.info("👍 **Bom Fit Presencial!** Adaptação sólida à rotina corporativa física.")
        else:
            st.warning("⚠️ **Atenção ao Modelo:** Considere o impacto da rotina física no seu bem-estar.")

    st.markdown("---")
    st.markdown("### 💼 Portais de Vagas Presenciais e Híbridas")
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        with st.container(border=True):
            st.markdown("#### 🔗 LinkedIn")
            st.markdown("[🔗 Acessar LinkedIn](https://www.linkedin.com/)")
    with col_p2:
        with st.container(border=True):
            st.markdown("#### 🏢 Gupy & Catho")
            st.markdown("[🔗 Acessar Gupy](https://www.gupy.io/)")
            st.markdown("[🔗 Acessar Catho](https://catho.com.br/)")
    with col_p3:
        with st.container(border=True):
            st.markdown("#### 📋 InfoJobs")
            st.markdown("[🔗 Acessar InfoJobs](https://www.infojobs.com.br/)")

    st.markdown("---")
    st.text_area("Notas de progresso na Fase 4 (*Obrigatório preencher para avançar*)", key='resultado_fase4', height=150)

    st.markdown("---")
    col_bt1, col_bt2, col_bt3 = st.columns([1, 1, 4])
    with col_bt1:
         if st.button("Voltar à Fase 3", key='btn_f4_voltar'):
            st.session_state['pagina_atual'] = 'Fase3'
            st.rerun()
    with col_bt3:
        if st.button("Avançar para Fase 5: Upskilling, Currículo, Apoio e Oportunidades", key='btn_f4_avancar', type="primary"):
            if not st.session_state.get('resultado_fase4'):
                st.warning("⚠️ **Atenção:** Preencha as notas de progresso da Fase 4 para prosseguir.")
            else:
                st.session_state['fase4_concluida'] = True
                st.session_state['pagina_atual'] = 'Fase5'
                st.rerun()

def pagina_fase5():
    if not st.session_state.get('fase4_concluida'):
        st.warning("🔒 **Acesso Bloqueado:** Conclua a Fase 4 preenchendo as notas de progresso antes de acessar esta etapa final.")
        if st.button("Ir para Fase 4"):
            st.session_state['pagina_atual'] = 'Fase4'
            st.rerun()
        return

    st.header("Fase 5: Trilha de Upskilling, Currículo Humano, Rede de Apoio e Oportunidades")
    st.markdown("---")
    
    # PASSO 3: Upskilling
    st.markdown("### 📚 Passo 3: A Trilha de Capacitação (Upskilling)")
    st.write("Identificou alguma lacuna técnica ou comportamental nas fases anteriores? Acesse plataformas de cursos gratuitos e de curta duração para elevar seu valor competitivo:")
    
    col_up1, col_up2 = st.columns(2)
    with col_up1:
        with st.container(border=True):
            st.markdown("#### 🛠️ Gestão, Ética e Compliance")
            st.markdown("- **Sebrae:** Cursos gratuitos de gestão e empreendedorismo ([Acessar](https://www.sebrae.com.br/))")
            st.markdown("- **Fundação Estudar / Labx:** Desenvolvimento de liderança e autoconhecimento")
            st.markdown("- **Coursera / FGV:** Trilhas abertas em Compliance, Governança e Ética Corporativa")
    with col_up2:
        with st.container(border=True):
            st.markdown("#### 💻 Habilidades Digitais e Produtividade")
            st.markdown("- **Microsoft Learn / LinkedIn Learning:** Ferramentas digitais corporativas")
            st.markdown("- **Fundação Bradesco:** Cursos gratuitos de tecnologia e informática básica a avançada ([Acessar](https://www.ev.org.br/))")

    st.markdown("---")

    # PASSO 4: Currículo Enxuto e Humano
    st.markdown("### 📄 Passo 4: O Currículo Enxuto e Humano")
    st.write("Esqueça os modelos engessados e cheios de buzzwords que geram barreiras automáticas em sistemas de IA (ATS). Siga estas diretrizes práticas para um currículo simples e focado em entregas:")

    with st.container(border=True):
        st.markdown("""
        - **1. Layout Limpo e Direto:** Use uma única página (ou no máximo duas se muita experiência). Fontes limpas (Arial, Calibri) e sem blocos coloridos complexos que travam os leitores automáticos.
        - **2. Foco em Entregas (Resultados):** Em vez de listar apenas funções antigas, descreva o que você **entregou ou melhorou**. Ex: *'Reestruturação de fluxo de conformidade que reduziu em 20% o tempo de resposta a auditorias.'*
        - **3. Alinhamento Comportamental (*Behavioral*):** Destaque clareza na resolução de problemas, capacidade de adaptação e postura ética em momentos de crise.
        - **4. Conecte com o Propósito:** Um breve resumo inicial mostrando quem você é profissionalmente e qual o seu foco atual de carreira.
        """)

    st.markdown("---")

    # REDE DE APOIO PSICOLÓGICO
    st.markdown("### 🧠 Rede de Apoio Psicológico e Saúde Mental")
    st.write("A transição e a pressão de processos seletivos podem ser emocionalmente desafiadoras. Cuidar da mente é parte fundamental do desenvolvimento profissional:")

    with st.container(border=True):
        st.markdown("""
        - **CVV (Centro de Valorização da Vida):** Apoio emocional e prevenção do suicídio gratuito, sigiloso e 24h por dia. 
          - **Ligue:** 188 | **Chat:** [cvv.org.br](https://www.cvv.org.br/)
        - **Clínicas-Escola de Psicologia:** Muitas faculdades e universidades oferecem atendimento psicológico gratuito ou social à comunidade.
        - **Aplicativos e Práticas de Autocuidado:** Reserve momentos de pausas conscientes, pausas na tela e atividades físicas leves para regular o estresse do dia a dia.
        """)

    st.markdown("---")

    # --- MONETIZAÇÃO 1: BANCO DE TALENTOS B2B (RECRUTAMENTO) ---
    st.markdown("### 🤝 Oportunidades Exclusivas: Banco de Talentos ICODS (B2B)")
    with st.container(border=True):
        st.markdown("""
        O uso de toda a plataforma, diagnóstico e trilhas é **100% gratuito** para você. 
        Como forma de acelerar sua contratação, mantemos um **Banco de Talentos B2B** exclusivo, onde empresas parceiras que buscam profissionais éticos com formação em compliance buscam perfis pré-qualificados.
        """)
        
        st.checkbox(
            "✔️ **Autorizo o envio do meu perfil comportamental e currículo** para o Banco de Talentos Exclusivo ICODS, para ser conectado a oportunidades de empresas parceiras.",
            key='optin_banco_talentos'
        )
        if st.session_state['optin_banco_talentos']:
            st.success("🎉 **Perfil Autorizado!** Seus dados e alinhamento comportamental foram integrados com sucesso ao nosso pool de talentos parceiros.")

    st.markdown("---")

    # --- MONETIZAÇÃO 2: SERVIÇOS DE ALTO VALOR (UPSELLING) ---
    st.markdown("### 💎 Aceleração Profissional: Serviços de Alto Valor (Upselling)")
    st.write("Quer um acompanhamento mais profundo, direcionado e personalizado para garantir sua aprovação nos processos seletivos mais exigentes?")

    col_mon1, col_mon2 = st.columns(2)
    with col_mon1:
        with st.container(border=True):
            st.markdown("#### 🎯 Mentoria Individual de Carreira")
            st.markdown("Sessões online individuais de orientação profissional e **simulação de entrevista de compliance** diretamente com especialistas.")
            st.markdown("- **Foco:** Prática de postura em dilemas éticos, técnicas de entrevista e posicionamento.")
            if st.button("Quero Saber Mais sobre Mentoria", key='btn_mentoria'):
                st.info("💡 Entre em contato pelo e-mail **icods.parceiros@gmail.com** para agendar sua sessão de mentoria individual.")
    with col_mon2:
        with st.container(border=True):
            st.markdown("#### 📝 Análise de Currículo Personalizada")
            st.markdown("Um serviço humano de revisão e reescrita cirúrgica do seu currículo para focar em entregas e evitar barreiras de IA (ATS).")
            st.markdown("- **Foco:** Transformar descrições vagas em um histórico magnético de resultados.")
            if st.button("Quero Análise de Currículo", key='btn_curriculo'):
                st.info("💡 Envie seu currículo atual para **icods.curriculos@gmail.com** e nossa equipe especializada fará a reestruturação.")

    st.markdown("---")
    st.text_area("Notas e plano de ação final (Fase 5) (*Obrigatório preencher para gerar o relatório*)", key='resultado_fase5', height=150, placeholder="Escreva seus próximos passos de capacitação, ajustes no currículo e compromissos de autocuidado...")

    st.markdown("---")
    col_bt1, col_bt2, col_bt3 = st.columns([1, 1, 4])
    with col_bt1:
         if st.button("Voltar à Fase 4", key='btn_f5_voltar'):
            st.session_state['pagina_atual'] = 'Fase4'
            st.rerun()
    with col_bt3:
        if st.button("Gerar Relatório Final de Desenvolvimento", key='btn_gerar_relatorio', type="primary"):
            if not st.session_state.get('resultado_fase5'):
                st.warning("⚠️ **Atenção:** Preencha o plano de ação final na Fase 5 para consolidar seu relatório.")
            else:
                st.session_state['fase5_concluida'] = True
                st.session_state['pagina_atual'] = 'Relatorio'
                st.rerun()

def pagina_relatorio():
    if not st.session_state.get('fase5_concluida'):
        st.warning("🔒 **Acesso Bloqueado:** Conclua todas as fases anteriores para visualizar o relatório final.")
        if st.button("Ir para Fase 5"):
            st.session_state['pagina_atual'] = 'Fase5'
            st.rerun()
        return

    st.header("📋 Relatório Final: Trilha ICODS de Behavioral Compliance")
    st.markdown("---")
    st.write("Parabéns por concluir a jornada! Abaixo está o consolidado do seu diagnóstico profissional, alinhamento comportamental e plano de ação.")

    interesses_str = ", ".join(st.session_state.get('interesses', []))
    relatorio_texto = f"""==================================================
RELATÓRIO DE DESENVOLVIMENTO PROFISSIONAL - ICODS
==================================================

1. DADOS CADASTRAIS E PERFIL
- Nome: {st.session_state.get('nome')}
- Formação: {st.session_state.get('formacao')}
- Experiência Principal: {st.session_state.get('experiencia')}
- Região: {st.session_state.get('contexto_regiao')}
- Áreas de Interesse: {interesses_str}
- Ambiente Ideal: {st.session_state.get('ambiente_ideal')}

2. TOMADA DE DECISÃO ÉTICA (DILEMA SIMULADO)
- Escolha no cenário prático: Opção {st.session_state.get('cenario_simulado')}
- Reflexão / Dilema Real relatado: {st.session_state.get('questao_etica', 'Nenhuma reflexão adicional registrada.')}

3. NOTAS DE PROGRESSO POR FASE
- Fase 2 (Inteligência de Mercado): {st.session_state.get('resultado_fase2')}
- Fase 3 (Ecossistema Virtual / Remoto): {st.session_state.get('resultado_fase3')}
- Fase 4 (Ecossistema Presencial / Híbrido): {st.session_state.get('resultado_fase4')}
- Fase 5 (Upskilling e Plano de Ação): {st.session_state.get('resultado_fase5')}

4. AUTORIZAÇÃO BANCO DE TALENTOS B2B
- Opt-in Autorizado: {'Sim' if st.session_state.get('optin_banco_talentos') else 'Não'}

==================================================
© 2026 | ICODS - Plataforma de Behavioral Compliance
==================================================
"""

    with st.container(border=True):
        st.markdown(f"### 👤 Perfil: {st.session_state.get('nome')}")
        st.markdown(f"**Formação:** {st.session_state.get('formacao')} | **Experiência:** {st.session_state.get('experiencia')}")
        st.markdown(f"**Localidade:** {st.session_state.get('contexto_regiao')} | **Áreas de Interesse:** {interesses_str}")
        st.markdown(f"**Ambiente Desejado:** {st.session_state.get('ambiente_ideal')}")
    
    with st.container(border=True):
        st.markdown("### ⚙️ Síntese Comportamental e Notas das Fases")
        st.markdown(f"**Reflexão Fase 2:** {st.session_state.get('resultado_fase2')}")
        st.markdown(f"**Reflexão Fase 3:** {st.session_state.get('resultado_fase3')}")
        st.markdown(f"**Reflexão Fase 4:** {st.session_state.get('resultado_fase4')}")
        st.markdown(f"**Plano de Ação (Fase 5):** {st.session_state.get('resultado_fase5')}")

    st.markdown("---")
    
    st.download_button(
        label="📥 Descarregar Relatório Completo (.txt)",
        data=relatorio_texto,
        file_name="Relatorio_Desenvolvimento_ICODS.txt",
        mime="text/plain",
        type="primary"
    )

    st.markdown("---")
    col_bt1, col_bt2 = st.columns(2)
    with col_bt1:
        if st.button("Voltar à Fase 5"):
            st.session_state['pagina_atual'] = 'Fase5'
            st.rerun()
    with col_bt2:
        if st.button("Reiniciar Todo o Processo", key='btn_rel_reiniciar'):
            st.session_state.clear()
            st.session_state['pagina_atual'] = 'Inicio'
            st.rerun()

# --- FLUXO DE NAVEGAÇÃO PRINCIPAL ---
pagina_atual = st.session_state['pagina_atual']

if pagina_atual == 'Inicio':
    pagina_inicio()
elif pagina_atual == 'Diagnostico':
    pagina_diagnostico()
elif pagina_atual == 'Fase2':
    pagina_fase2()
elif pagina_atual == 'Fase3':
    pagina_fase3()
elif pagina_atual == 'Fase4':
    pagina_fase4()
elif pagina_atual == 'Fase5':
    pagina_fase5()
elif pagina_atual == 'Relatorio':
    pagina_relatorio()

# --- RODAPÉ ---
st.markdown("---")
st.markdown("© 2026 | ICODS - Plataforma de Desenvolvimento Behavioral Compliance e Oportunidades")
