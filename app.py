import streamlit as st
from PIL import Image
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Plataforma ICODS - Trilha de Desenvolvimento", layout="wide")

# --- INICIALIZAÇÃO DO SESSION STATE ---
paginas_validas = ['Inicio', 'Diagnostico', 'Fase2', 'Fase3']
if 'pagina_atual' not in st.session_state or st.session_state['pagina_atual'] not in paginas_validas:
    st.session_state['pagina_atual'] = 'Inicio'

# Inicialização dos dados do usuário
if 'nome' not in st.session_state: st.session_state['nome'] = ''
if 'formacao' not in st.session_state: st.session_state['formacao'] = ''
if 'experiencia' not in st.session_state: st.session_state['experiencia'] = ''
if 'interesses' not in st.session_state: st.session_state['interesses'] = []
if 'estilo' not in st.session_state: st.session_state['estilo'] = 'Analítico'
if 'questao_etica' not in st.session_state: st.session_state['questao_etica'] = ''

# Variáveis para armazenar os resultados das novas fases
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
    st.subheader("Dados Profissionais")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Nome Completo", key='nome')
        st.text_input("Formação Acadêmica", key='formacao')
    with col2:
        st.text_input("Área de Experiência Principal", key='experiencia')
        st.multiselect("Áreas de Interesse Profissional", ["Compliance", "Direito", "RH", "Gestão", "Tecnologia"], key='interesses')
    st.markdown("---")
    st.subheader("Diagnóstico Rápido de Estilo")
    st.radio("Como você descreve o seu estilo de trabalho?", ["Analítico", "Colaborativo", "Dinâmico", "Liderança"], key='estilo')
    st.markdown("---")
    st.text_area("Descreva uma situação que considera um dilema ético na sua carreira (Opcional)", key='questao_etica')
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
    
    # Inserção do painel de Inteligência de Mercado (Raio-X CAGED/IBGE)
    st.markdown("""
    <style>
        .market-intelligence-section {
            background: #ffffff;
            padding: 1rem 0;
        }
        .indicators-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }
        .indicator-card {
            background: #f8fafc;
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid #e2e8f0;
        }
        .indicator-card h3 {
            font-size: 1.1rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 0.75rem;
        }
        .indicator-card p {
            font-size: 0.9rem;
            color: #475569;
            margin-bottom: 0.5rem;
            text-align: justify;
        }
        .career-decision-box {
            background: rgba(45, 212, 191, 0.1);
            border-left: 4px solid #0d9488;
            padding: 1.25rem;
            border-radius: 0 12px 12px 0;
        }
        .career-decision-box h4 {
            color: #0f172a;
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .career-decision-box p {
            color: #334155;
            font-size: 0.9rem;
            margin: 0;
            text-align: justify;
        }
    </style>

    <section class="market-intelligence-section">
        <div class="container">
            <div class="section-header">
                <h3>📊 Raio-X do Mercado na sua Região</h3>
                <p>Entenda o cenário real de empregabilidade (dados oficiais do CAGED/IBGE) para decidir onde investir seu tempo e sua carreira no Agreste Pernambucano.</p>
            </div>

            <div class="indicators-grid">
                <div class="indicator-card">
                    <h3>📈 Perfil de Contratações</h3>
                    <p><strong>Destaque por Faixa Etária:</strong> Maior volume de vagas formais concentrado na faixa de 18 a 29 anos.</p>
                    <p><strong>Recorte de Gênero/Raça:</strong> Panorama atual das admissões formais na região.</p>
                </div>
                
                <div class="indicator-card">
                    <h3>🏭 Setores que Mais Empregam</h3>
                    <p>1. <strong>Indústria de Transformação</strong> (Calçados, Metalmecânica, Alimentos)</p>
                    <p>2. <strong>Comércio Varejista e Atacadista</strong></p>
                    <p>3. <strong>Serviços e Agroindústria</strong></p>
                </div>
            </div>

            <div class="career-decision-box">
                <h4>💡 Dica de Direcionamento Profissional</h4>
                <p>Se a sua área pretendida apresenta baixa empregabilidade na região, o app te ajuda a identificar competências transferíveis para os setores que estão contratando ativamente no seu "quintal".</p>
            </div>
        </div>
    </section>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.write("### Notas e Alinhamento Profissional")
    st.text_area("Notas de progresso na Fase 2", key='resultado_fase2', height=150, placeholder="Escreva suas reflexões sobre as oportunidades mapeadas na região...")

    st.markdown("---")
    # Botões de navegação
    col_bt1, col_bt2, col_bt3 = st.columns([1, 1, 4])
    with col_bt1:
         if st.button("Voltar ao Diagnóstico", key='btn_f2_voltar'):
            st.session_state['pagina_atual'] = 'Diagnostico'
            st.rerun()
    with col_bt3:
        if st.button("Finalizar e Ir para Fase 3", key='btn_f2_avancar', type="primary"):
            st.session_state['pagina_atual'] = 'Fase3'
            st.rerun()

def pagina_fase3():
    st.header("Fase 3: Conclusão e Plano de Ação")
    st.markdown("---")
    st.write("### Conteúdo da Fase 3")
    st.success("🎉 Parabéns por chegar até aqui! Resumo do seu perfil:")

    # Exibindo dados básicos do diagnóstico
    st.write(f"**Nome:** {st.session_state['nome']}")
    st.write(f"**Estilo:** {st.session_state['estilo']}")
    st.info("⚠️ **Área de Edição:** Insira aqui o plano de ação final, certificado ou recomendações baseadas no perfil.")

    st.text_area("Plano de Ação Individual (PAI)", key='resultado_fase3', height=150, placeholder="Defina seus próximos passos...")

    st.markdown("---")
    col_bt1, col_bt2 = st.columns([1, 5])
    with col_bt1:
         if st.button("Voltar para Fase 2", key='btn_f3_voltar'):
            st.session_state['pagina_atual'] = 'Fase2'
            st.rerun()

    st.markdown("---")
    if st.button("Reiniciar Todo o Processo (Voltar ao Início)", key='btn_f3_reiniciar'):
        st.session_state['nome'] = ''
        st.session_state['formacao'] = ''
        st.session_state['experiencia'] = ''
        st.session_state['interesses'] = []
        st.session_state['estilo'] = 'Analítico'
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
