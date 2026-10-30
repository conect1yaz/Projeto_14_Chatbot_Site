
import os
from pathlib import Path

import streamlit as st
from groq import Groq
from dotenv import load_dotenv


# =====================================================
# 1. CONFIGURAÇÕES DO STREAMLIT
# =====================================================

st.set_page_config(
    page_title="CLICK AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# 2. CAMINHOS E API
# =====================================================

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"

load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "openai/gpt-oss-120b"

client = Groq(api_key=API_KEY) if API_KEY else None


# =====================================================
# 3. CARREGAMENTO DO CSS
# =====================================================

css_path = ASSETS_DIR / "style.css"

if css_path.exists():

    with open(css_path, "r", encoding="utf-8") as arquivo:
        css = arquivo.read()

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )


# =====================================================
# 4. PERSONALIDADE DO CLICK AI
# =====================================================

SYSTEM_PROMPT = """
Você é o CLICK AI, um assistente virtual inteligente,
criativo, curioso e amigável.

Sua personalidade:
- Seja educado e prestativo.
- Explique assuntos complexos de maneira simples.
- Organize suas respostas quando necessário.
- Utilize exemplos para facilitar o aprendizado.
- Seja criativo e interessante.
- Adapte sua linguagem ao usuário.
- Responda no idioma utilizado na pergunta.
"""


# =====================================================
# 5. INICIALIZAÇÃO DAS CONVERSAS
# =====================================================

if "conversations" not in st.session_state:

    st.session_state.conversations = {
        "Conversa 1": []
    }


if "active_chat" not in st.session_state:

    st.session_state.active_chat = "Conversa 1"


if "pending_prompt" not in st.session_state:

    st.session_state.pending_prompt = None


# Recupera as mensagens da conversa selecionada

messages = st.session_state.conversations[
    st.session_state.active_chat
]


# =====================================================
# 6. FUNÇÕES AUXILIARES
# =====================================================

def nova_conversa():

    numero = len(st.session_state.conversations) + 1
    nome = f"Conversa {numero}"

    st.session_state.conversations[nome] = []
    st.session_state.active_chat = nome


def enviar_mensagem(pergunta):

    # Guarda a pergunta do usuário
    messages.append({
        "role": "user",
        "content": pergunta
    })

    # Verifica a chave da API
    if not client:

        st.error(
            "Chave da Groq não encontrada. "
            "Confira seu arquivo .env."
        )

        messages.pop()
        return

    try:

        # Solicita resposta à Groq
        resposta = client.chat.completions.create(

            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                *messages
            ],

            temperature=0.7,
            max_completion_tokens=2048
        )

        texto = (
            resposta.choices[0].message.content
            or "Não consegui gerar uma resposta."
        )

        # Guarda a resposta da IA
        messages.append({
            "role": "assistant",
            "content": texto
        })

    except Exception as erro:

        messages.pop()

        st.error(
            f"Não foi possível obter uma resposta: {erro}"
        )


# =====================================================
# 7. SIDEBAR
# =====================================================

with st.sidebar:

    # Logo
    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">🚀</div>

            <div>
                <div class="logo-click">
                    CLICK<span>.AI</span>
                </div>

                <p>Seu assistente virtual criativo</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Nova conversa
    if st.button(
        "＋  Nova conversa",
        use_container_width=True,
        key="nova_conversa"
    ):

        nova_conversa()
        st.rerun()

    # Início
    if st.button(
        "⌂  Início",
        use_container_width=True,
        key="inicio"
    ):

        st.session_state.active_chat = "Conversa 1"
        st.rerun()

    # Histórico
    st.markdown(
        """
        <div class="history-label">
            CONVERSAS RECENTES
        </div>
        """,
        unsafe_allow_html=True
    )

    for nome in reversed(
        list(st.session_state.conversations.keys())
    ):

        if nome == st.session_state.active_chat:
            prefixo = "✦"
        else:
            prefixo = "◇"

        if st.button(
            f"{prefixo}  {nome}",
            key=f"historico_{nome}",
            use_container_width=True
        ):

            st.session_state.active_chat = nome
            st.rerun()

    st.markdown("---")

    # Card inferior
    st.markdown(
        """
        <div class="sidebar-card">

            <div class="sidebar-rocket">🚀</div>

            <h4>CLICK AI</h4>

            <p>✦ Powered by Groq</p>

            <div class="sidebar-phrase">
                Grandes ideias começam
                com uma boa conversa ♡
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# 8. CABEÇALHO PRINCIPAL
# =====================================================

col1, col2 = st.columns([3, 1])

with col1:

    st.markdown(
        """
        <div class="ai-status">
            <span class="status-dot"></span>
            CLICK AI • ASSISTENTE VIRTUAL
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
        <div class="model-label">
            ✦ GPT-OSS 120B
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# 9. TELA INICIAL
# =====================================================

if not messages:

    col_mascote, col_apresentacao = st.columns(
        [0.95, 1.35],
        gap="medium"
    )

    # Mascote
    with col_mascote:

        mascot_path = ASSETS_DIR / "astronauta.png"

        if mascot_path.exists():

            st.image(
                str(mascot_path),
                width=390
            )

        else:

            st.html(
                """
                <div class="mascot-placeholder">
                    🚀
                </div>
                """
            )

    # Apresentação
    with col_apresentacao:

        st.html(
            """
            <div class="welcome">

                <h1>
                    CLICK<span>.AI</span>
                </h1>

                <h2>
                    Olá, seja bem-vindo(a)!
                </h2>

                <p>
                    Eu sou o CLICK AI, seu assistente virtual
                    criativo e curioso, pronto para te ajudar
                    a explorar ideias, descobrir novos mundos
                    e transformar suas perguntas em grandes ideias!
                </p>

                <div class="welcome-decoration">
                    ✧ Sonhe. Pergunte. Explore. ♡
                </div>

            </div>
            """
        )

    # Sugestões
    st.html(
        """
        <div class="suggestion-title">
            ✦ POR ONDE VAMOS COMEÇAR?
        </div>
        """
    )

    col1, col2 = st.columns(2, gap="medium")

    with col1:

        if st.button(
            "💡  Aprender algo novo",
            use_container_width=True
        ):

            st.session_state.pending_prompt = (
                "Quero aprender algo novo. "
                "Me apresente um assunto interessante."
            )

            st.rerun()

        if st.button(
            "✨  Criar uma ideia",
            use_container_width=True
        ):

            st.session_state.pending_prompt = (
                "Ajude-me a desenvolver uma ideia criativa."
            )

            st.rerun()

    with col2:

        if st.button(
            "💻  Explorar tecnologia",
            use_container_width=True
        ):

            st.session_state.pending_prompt = (
                "Quais tecnologias estão transformando o mundo?"
            )

            st.rerun()

        if st.button(
            "💬  Tirar uma dúvida",
            use_container_width=True
        ):

            st.session_state.pending_prompt = (
                "Quero tirar uma dúvida. Vamos começar!"
            )

            st.rerun()


# =====================================================
# 10. HISTÓRICO DE MENSAGENS
# =====================================================

else:

    st.markdown(
        """
        <div class="chat-heading">
            <h2>✦ Nossa conversa</h2>
            <p>Explore suas ideias com o CLICK AI.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    for mensagem in messages:

        if mensagem["role"] == "user":

            avatar = "👤"

        else:

            avatar = "🚀"

        with st.chat_message(
            mensagem["role"],
            avatar=avatar
        ):

            st.markdown(mensagem["content"])


# =====================================================
# 11. CAMPO DE MENSAGEM
# =====================================================

prompt = st.chat_input(
    "Digite sua mensagem para o CLICK AI..."
)

# Verifica se o usuário escolheu uma sugestão

if st.session_state.pending_prompt:

    prompt = st.session_state.pending_prompt

    st.session_state.pending_prompt = None


# =====================================================
# 12. PROCESSAMENTO DA MENSAGEM
# =====================================================

if prompt:

    # Exibe a pergunta
    with st.chat_message("user", avatar="👤"):

        st.markdown(prompt)

    # Processa a resposta
    with st.chat_message("assistant", avatar="🚀"):

        with st.spinner("O CLICK AI está pensando..."):

            enviar_mensagem(prompt)

        # Exibe a resposta mais recente
        if messages and messages[-1]["role"] == "assistant":

            st.markdown(messages[-1]["content"])

    # Atualiza a interface
    st.rerun()


# =====================================================
# 13. RODAPÉ
# =====================================================

st.html(
    """
    <div class="footer">
        CLICK AI © 2026 • Grandes ideias começam aqui ✦
    </div>
    """
)
