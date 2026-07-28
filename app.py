import streamlit as st
from PIL import Image
import os
import textwrap
from supabase import create_client

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Plataforma ICODS - Trilha de Desenvolvimento", layout="wide")

# --- CONEXÃO COM O SUPABASE ---
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()

# --- INICIALIZAÇÃO DO SESSION STATE ---
paginas_validas = ['Inicio', 'Diagnostico', 'Fase2', 'Fase3']
if 'pagina_atual' not in st.session_state or st.session_state['pagina_atual'] not in paginas_validas:
    st.session_state['pagina_atual'] = 'Inicio'

# Inicialização dos dados do usuário (Fase 1 e demais)
if 'nome' not in st.session_state: st.session_state['nome'] = ''
if 'formacao' not in st.session_state: st.session_state['formacao'] = ''
if 'experiencia' not in st.session_state: st.session_state['experiencia'] = ''
if 'interesses' not in st.session_state: st.session_state['interesses'] = []
if 'contexto_regiao' not in st.session_state: st.session_state['contexto_regiao'] = ''
if 'ambiente_ideal' not in st.session_state: st.session_state['ambiente_ideal'] = ''
if 'cenario_simulado' not in st.session_state: st.session_state['cenario_simulado'] = 0
if 'questao_etica' not in st.session_state: st.session_state['questao_etica'] = ''

# Variáveis para armazenar os resultados das fases
if 'resultado_fase2' not in st.session_state: st.session_state['resultado_fase2'] = ''
if 'resultado_fase3' not in st.session_state: st.session_state['resultado_fase3'] = ''

# --- FUNÇÃO PARA CARREGAR IMAGENS COM SEGURANÇA ---
def carregar_imagem(nome_arquivo):
    """Carrega uma imagem da pasta local (raiz)."""
    try:
        diretorio_atual = os.getcwd()
        caminho_completo = os.path.join(diretorio_atual, nome_arquivo)

        if os.path.exists(caminho_completo):
            return Image.open(caminho_completo)
        else:
            st.warning(f"Aviso: A imagem '{nome_arquivo}' não foi encontrada em '{diretorio_atual}'.")
            return None
    except Exception as e:
        st.error(f"Erro crítico ao carregar imagem {nome_arquivo}: {e}")
        return None

# --- DEFINIÇÃO DAS PÁGINAS (FUNÇÕES) ---

def pagina_inicio():
    st.title("Trilha de Orientação Profissional")
    st.markdown("---")
    img_inicio = carregar_imagem("fot_fundo.jpg")
    if img_inicio:
        st.image(img_inicio, caption="ICODS - Desenvolvimento Comportamental", width=400)
    st.markdown("""
    ### Bem-vindo(a) à sua jornada de desenvolvimento.
    Esta plataforma foi desenhada para o apoiar no desenvolvimento da sua carreira,
    aliando o seu perfil comportamental a práticas éticas de compliance.

    Utilize os botões abaixo para navegar entre as fases do programa.
    """)
    st.markdown("---")
    if st.button("Iniciar Diagnóstico", key='btn_inicio_diag', type="primary"):
        st.session_state['pagina_atual'] = 'Diagnostico'
        st.rerun()

def pagina_diagnostico():
    st.header("Fase 1: Diagnóstico Comportamental e de Carreira")
    st.markdown("---")
    
    # --- CAMADA 1: Aspirações, Interesses e Contexto ---
    st.subheader("📌 Camada 1: Aspirações, Contexto e Alinhamento de Valores")
    st.write("Mapeie suas preferências profissionais, áreas de interesse e o cenário contextual em que você atua.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Nome Completo", key='nome')
        st.text_input("Formação Acadêmica", key='formacao')
        st.multiselect("Áreas de Interesse Profissional", ["Compliance", "Direito", "RH", "Gestão", "Tecnologia", "Operações"], key='interesses')
    with col2:
        st.text_input("Área de Experiência Principal", key='experiencia')
        st.text_input("Cidade e Estado onde Reside (Contexto Regional)", key='contexto_regiao')
        st.text_input("Ambiente Corporativo Ideal (Ex: Colaborativo, Estruturado, Inovador)", key='ambiente_ideal')

    st.markdown("---")
    
    # --- CAMADA 2: Cenários Simulados de Tomada de Decisão ---
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

    # Botões de navegação
    col_bt1, col_bt2, col_bt3 = st.columns([1, 1, 4])
    with col_bt1:
         if st.button("Voltar ao Início", key='btn_diag_voltar'):
            st.session_state['pagina_atual'] = 'Inicio'
            st.rerun()
    with col_bt3:
        if st.button("Avançar para Fase 2: Raio-X e Oportunidades", key='btn_diag_avancar', type="primary"):
            st.session_state['pagina_atual'] = 'Fase2'
            st.rerun()

def pagina_fase2():
    st.header("Fase 2: Inteligência de Mercado e Oportunidades Locais")
    st.markdown("---")

    st.markdown("### 📊 Raio-X do Mercado por Região")
    st.write("Selecione a região, o estado e o município desejado para consultar os indicadores oficiais de empregabilidade.")

    # Buscar todos os registros do banco para montar a hierarquia dinamicamente
    try:
        response_all = supabase.table("indicadores_regionais").select("regiao, estado, cidade").execute()
        dados_db = response_all.data if response_all.data else []
    except Exception as e:
        dados_db = []
        st.error(f"Erro ao carregar dados do Supabase: {e}")

    if not dados_db:
        st.warning("⚠️ Nenhum indicador regional encontrado no banco de dados. Insira dados na tabela `indicadores_regionais` para iniciar.")
    else:
        # 1. Seletor de Região dinâmico baseado apenas em registros existentes
        regioes_disponiveis = sorted(list(set(item["regiao"] for item in dados_db if item.get("regiao"))))
        regiao_selecionada = st.selectbox("Selecione a Região:", regioes_disponiveis)

        # 2. Seletor de Estado dinâmico filtrado pela Região selecionada
        estados_disponiveis = sorted(list(set(item["estado"] for item in dados_db if item.get("regiao") == regiao_selecionada and item.get("estado"))))
        
        if estados_disponiveis:
            estado_selecionado = st.selectbox("Selecione o Estado:", estados_disponiveis)

            # 3. Seletor de Município dinâmico filtrado pelo Estado selecionado
            cidades_disponiveis = sorted(list(set(item["cidade"] for item in dados_db if item.get("estado") == estado_selecionado and item.get("cidade"))))
            
            if cidades_disponiveis:
                cidade_selecionada = st.selectbox("Selecione o Município:", cidades_disponiveis)
                
                # Buscar dados completos do município escolhido
                response = supabase.table("indicadores_regionais").select("*").eq("cidade", cidade_selecionada).execute()
                dados = response.data[0] if response.data else None

                if dados:
                    st.info(f"📅 **Mês de Referência dos Dados:** {dados.get('mes_referencia', 'N/A')}")

                    faixa = dados.get('faixa_etaria', 'Sem dados cadastrados.')
                    genero = dados.get('genero_raca', 'Sem dados cadastrados.')
                    setores = dados.get('setores_lideres', [])

                    st.markdown("---")
                    
                    # Layout em colunas nativas do Streamlit
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

                    st.success("💡 **Dica de Direcionamento Profissional:** O app cruza o seu perfil comportamental com a realidade econômica deste município para orientar suas transições de carreira.")

    st.markdown("---")
    st.write("### Notas e Alinhamento Profissional")
    st.text_area("Notas de progresso na Fase 2", key='resultado_fase2', height=150, placeholder="Escreva suas reflexões sobre as oportunidades mapeadas...")

    st.markdown("---")
    # Botões de navegação
    col_bt1, col_bt2, col_bt3 = st.columns([1, 1, 4])
    with col_bt1:
         if st.button("Voltar ao Diagnóstico", key='btn_f2_voltar'):
            st.session_state['pagina_atual'] = 'Diagnostico'
            st.rerun()
    with col_bt3:
        if st.button("Avançar para Fase 3: Trabalho Remoto", key='btn_f2_avancar', type="primary"):
            st.session_state['pagina_atual'] = 'Fase3'
            st.rerun()

def pagina_fase3():
    st.header("Fase 3: O Ecossistema Virtual e de Trabalho Remoto")
    st.markdown("---")
    
    st.markdown("### 🌐 Rompendo Barreiras Geográficas")
    st.write("Esta fase expande suas oportunidades para além do mercado local, conectando você a vagas de trabalho remoto em todo o país e avaliando sua prontidão para o modelo home office.")

    # 1. Avaliação de Afinidade e Ferramentas Básicas para Trabalho Remoto
    st.markdown("#### 🔍 Avaliação de Prontidão para o Trabalho Remoto")
    st.write("Marque os itens abaixo para verificar seu nível de adequação e infraestrutura técnica e comportamental para o formato à distância:")

    with st.container(border=True):
        col_f3_1, col_f3_2 = st.columns(2)
        
        with col_f3_1:
            st.markdown("**Infraestrutura Tecnológica**")
            internet = st.checkbox("Possuo internet banda larga estável", key="rem_internet")
            computador = st.checkbox("Computador/Notebook em bom estado de funcionamento", key="rem_pc")
            espaco = st.checkbox("Espaço físico adequado e silencioso para trabalho em casa", key="rem_espaco")
            
        with col_f3_2:
            st.markdown("**Perfil Comportamental e Autonomia**")
            autonomia = st.checkbox("Tenho facilidade para gerenciar meu próprio tempo e prazos", key="rem_autonomia")
            comunicacao = st.checkbox("Boa comunicação escrita e digital (Slack, Teams, Zoom, etc.)", key="rem_comunicacao")
            aprendizado = st.checkbox("Disposição para aprendizado contínuo de novas ferramentas digitais", key="rem_aprendizado")

        # Cálculo dinâmico da pontuação de prontidão
        itens_checados = sum([internet, computador, espaco, autonomia, comunicacao, aprendizado])
        
        st.markdown("---")
        if itens_checados == 6:
            st.success("🌟 **Prontidão Excelente!** Você possui todos os requisitos ideais de infraestrutura e perfil para atuar com alta performance em regime remoto.")
        elif itens_checados >= 4:
            st.info("👍 **Boa Prontidão!** Você tem uma base sólida, mas vale atentar para os itens ainda não marcados para mitigar eventuais gargalos à distância.")
        else:
            st.warning("⚠️ **Atenção aos Requisitos:** O trabalho remoto exige autonomia e ferramentas específicas. Considere estruturar os pontos pendentes para ampliar suas chances competitivas.")

    st.markdown("---")

    # 2. Seção Dedicada de Vagas Virtuais e Remotas (Plataformas Idôneas)
    st.markdown("### 💼 Portais e Plataformas Especializadas em Trabalho Remoto")
    st.write("Explore portais e ecossistemas de referência nacional e internacional que contratam em regime 100% home office ou híbrido:")

    col_plat1, col_plat2, col_plat3 = st.columns(3)

    with col_plat1:
        with st.container(border=True):
            st.markdown("#### 🚀 Remotar & Coodesh")
            st.markdown("Plataformas brasileiras focadas em conectar profissionais a vagas de tecnologia, produtos e operações remotas.")
            st.markdown("[🔗 Acessar Remotar](https://remotar.com.br/)")
            st.markdown("[🔗 Acessar Coodesh](https://coodesh.com/)")

    with col_plat2:
        with st.container(border=True):
            st.markdown("#### 💻 Tech & Digital")
            st.markdown("Portais voltados para desenvolvimento, suporte digital, atendimento e marketing em empresas inovadoras.")
            st.markdown("[🔗 Geek Hunter](https://www.geekhunter.com.br/)")
            st.markdown("[🔗 Trampos.co](https://trampos.co/)")

    with col_plat3:
        with st.container(border=True):
            st.markdown("#### 🌍 Ecossistema Global")
            st.markdown("Plataformas internacionais com forte presença de vagas remotas para falantes de português e espanhol.")
            st.markdown("[🔗 We Work Remotely](https://weworkremotely.com/)")
            st.markdown("[🔗 Remote.co](https://remote.co/)")

    st.markdown("---")
    st.write("### Notas e Alinhamento Profissional para o Home Office")
    st.text_area("Notas de progresso na Fase 3", key='resultado_fase3', height=150, placeholder="Escreva sua estratégia de posicionamento, ajustes necessários no currículo ou metas de capacitação digital...")

    st.markdown("---")
    # Botões de navegação
    col_bt1, col_bt2, col_bt3 = st.columns([1, 1, 4])
    with col_bt1:
         if st.button("Voltar à Fase 2", key='btn_f3_voltar'):
            st.session_state['pagina_atual'] = 'Fase2'
            st.rerun()
    with col_bt3:
        if st.button("Reiniciar Todo o Processo", key='btn_f3_reiniciar', type="primary"):
            st.session_state['nome'] = ''
            st.session_state['formacao'] = ''
            st.session_state['experiencia'] = ''
            st.session_state['interesses'] = []
            st.session_state['contexto_regiao'] = ''
            st.session_state['ambiente_ideal'] = ''
            st.session_state['cenario_simulado'] = 0
            st.session_state['questao_etica'] = ''
            st.session_state['resultado_fase2'] = ''
            st.session_state['resultado_fase3'] = ''
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

# --- RODAPÉ ---
st.markdown("---")
st.markdown("© 2026 | ICODS - Plataforma de Desenvolvimento Behavioral Compliance")
