import json
import os
import re
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, List, Tuple

import streamlit as st

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR = BASE_DIR / "data"
MANUAL_JSON = DATA_DIR / "manual_credenciape_paginas.json"
MANUAL_PDF = DATA_DIR / "manual_credenciape.pdf"
ENV_FILE = BASE_DIR / ".env"

AZUL_ESCURO = "#173B8F"
AZUL = "#235EE8"
AZUL_CLARO = "#EAF1FF"
VERDE = "#16A34A"
FUNDO_ESCURO = "#07111F"
SUPERFICIE = "#0D1B2E"
SUPERFICIE_2 = "#12243A"
BORDA_ESCURO = "#223B5F"
TEXTO_CLARO = "#F4F8FF"
TEXTO_MUTED = "#A9B8D0"

st.set_page_config(
    page_title="Assistente CredenciaPE",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    f"""
    <style>
    :root {{
        --azul-escuro: {AZUL_ESCURO};
        --azul: {AZUL};
        --azul-claro: {AZUL_CLARO};
        --verde: {VERDE};
        --fundo-escuro: {FUNDO_ESCURO};
        --superficie: {SUPERFICIE};
        --superficie-2: {SUPERFICIE_2};
        --borda-escuro: {BORDA_ESCURO};
        --texto-claro: {TEXTO_CLARO};
        --texto-muted: {TEXTO_MUTED};
    }}

    .stApp {{
        background: radial-gradient(circle at top right, rgba(35,94,232,.20), transparent 30%), linear-gradient(180deg, #07111F 0%, #0B1627 48%, #08111F 100%);
        color: var(--texto-claro);
    }}

    [data-testid="stSidebar"] {{
        background: #081526;
        border-right: 1px solid var(--borda-escuro);
    }}

    [data-testid="stSidebar"] * {{
        color: var(--texto-claro);
    }}

    h1, h2, h3, h4, h5, h6, p, label, span, div {{
        color: inherit;
    }}

    .main .block-container {{
        padding-top: 1.4rem;
        max-width: 1180px;
    }}

    .topbar {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 18px;
        padding: 18px 22px;
        background: rgba(13,27,46,0.92);
        border: 1px solid var(--borda-escuro);
        border-radius: 24px;
        box-shadow: 0 18px 42px rgba(0, 0, 0, .30);
        margin-bottom: 18px;
    }}

    .brand-title {{
        font-size: 1.65rem;
        font-weight: 850;
        color: var(--texto-claro);
        margin: 0;
        line-height: 1.1;
    }}

    .brand-subtitle {{
        color: var(--texto-muted);
        font-size: .96rem;
        margin-top: 6px;
    }}

    .hero {{
        padding: 28px;
        border-radius: 28px;
        background: radial-gradient(circle at top right, rgba(255,255,255,.12), transparent 32%), linear-gradient(135deg, #173B8F 0%, #235EE8 100%);
        color: #ffffff;
        box-shadow: 0 20px 55px rgba(23, 59, 143, .24);
        margin-bottom: 20px;
    }}

    .hero h1 {{
        font-size: clamp(1.8rem, 3vw, 3rem);
        line-height: 1.03;
        margin: 0 0 12px 0;
        font-weight: 900;
        letter-spacing: -0.04em;
    }}

    .hero p {{
        max-width: 760px;
        opacity: .92;
        font-size: 1.05rem;
        margin: 0;
    }}

    .pill-row {{
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 20px;
    }}

    .pill {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 9px 12px;
        border-radius: 999px;
        background: rgba(255,255,255,.14);
        border: 1px solid rgba(255,255,255,.22);
        font-size: .9rem;
        font-weight: 650;
    }}

    .info-card {{
        background: var(--superficie);
        border: 1px solid var(--borda-escuro);
        border-radius: 22px;
        padding: 18px;
        box-shadow: 0 16px 34px rgba(0, 0, 0, .24);
        height: 100%;
    }}

    .info-card h3 {{
        color: var(--texto-claro);
        margin-top: 0;
        font-size: 1.05rem;
    }}

    .small-muted {{
        color: var(--texto-muted);
        font-size: .92rem;
    }}

    .manual-status {{
        padding: 12px 14px;
        border-radius: 16px;
        background: rgba(35, 94, 232, .14);
        border: 1px solid rgba(83, 130, 246, .32);
        color: #DDE8FF;
        font-weight: 700;
        margin-bottom: 12px;
    }}

    .source-box {{
        background: var(--superficie-2);
        border: 1px solid var(--borda-escuro);
        border-radius: 16px;
        padding: 12px 14px;
        font-size: .92rem;
        color: var(--texto-claro);
        margin: 8px 0;
    }}

    .source-page {{
        display: inline-block;
        color: #ffffff;
        background: var(--azul-escuro);
        border-radius: 999px;
        padding: 2px 8px;
        font-size: .78rem;
        font-weight: 800;
        margin-bottom: 6px;
    }}

    .stChatMessage {{
        border-radius: 18px;
        background: rgba(13, 27, 46, .70);
        border: 1px solid rgba(34, 59, 95, .62);
    }}

    .stButton>button {{
        border-radius: 14px;
        border: 1px solid rgba(83, 130, 246, .40);
        background: var(--superficie-2);
        color: var(--texto-claro);
        font-weight: 750;
        min-height: 42px;
    }}

    .stButton>button:hover {{
        border-color: #7AA2FF;
        color: #ffffff;
        background: rgba(35, 94, 232, .30);
    }}

    .primary-note {{
        background: rgba(245, 158, 11, .12);
        border: 1px solid rgba(245, 158, 11, .38);
        color: #FFE8B6;
        border-radius: 16px;
        padding: 12px 14px;
        font-size: .92rem;
    }}

    .stTextInput input, .stChatInput textarea {{
        background: var(--superficie-2);
        border-color: var(--borda-escuro);
        color: var(--texto-claro);
    }}

    .stTextInput input:focus, .stChatInput textarea:focus {{
        border-color: #7AA2FF;
        box-shadow: 0 0 0 1px #7AA2FF;
    }}

    [data-testid="stMarkdownContainer"], [data-testid="stExpander"] {{
        color: var(--texto-claro);
    }}

    [data-testid="stExpander"] {{
        background: rgba(13, 27, 46, .60);
        border-color: var(--borda-escuro);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

STOPWORDS = {
    "a", "ao", "aos", "as", "ate", "até", "com", "como", "da", "das", "de", "do", "dos",
    "e", "em", "entre", "eu", "foi", "me", "na", "nas", "no", "nos", "o", "os", "ou",
    "para", "por", "pra", "que", "se", "sem", "sua", "suas", "seu", "seus", "um", "uma",
    "é", "sistema", "manual", "credenciape", "credencia", "pe", "quero", "preciso",
    "fazer", "faço", "faco", "clicar", "clique", "onde", "qual", "quais", "quando"
}


@st.cache_data(show_spinner=False)
def carregar_env_local() -> Dict[str, str]:
    """Carrega um arquivo .env simples sem depender de bibliotecas externas.

    Isso corrige o caso comum em que a chave foi colocada no .env,
    mas o Streamlit não leu automaticamente.
    """
    valores: Dict[str, str] = {}
    if not ENV_FILE.exists():
        return valores

    for linha in ENV_FILE.read_text(encoding="utf-8", errors="ignore").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, valor = linha.split("=", 1)
        chave = chave.strip()
        valor = valor.strip().strip('"').strip("'")
        if chave and valor:
            valores[chave] = valor
    return valores


def normalizar(texto: str) -> str:
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(ch for ch in texto if unicodedata.category(ch) != "Mn")
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def tokens_relevantes(texto: str) -> List[str]:
    normalizado = normalizar(texto)
    return [tok for tok in normalizado.split() if len(tok) >= 3 and tok not in STOPWORDS]


def quebrar_texto(texto: str, tamanho: int = 1800, overlap: int = 260) -> List[str]:
    texto = re.sub(r"\s+", " ", texto).strip()
    if not texto:
        return []
    if len(texto) <= tamanho:
        return [texto]

    partes = []
    inicio = 0
    while inicio < len(texto):
        fim = min(inicio + tamanho, len(texto))
        corte = texto.rfind(". ", inicio, fim)
        if corte == -1 or corte <= inicio + 500:
            corte = fim
        else:
            corte += 1
        partes.append(texto[inicio:corte].strip())
        if corte >= len(texto):
            break
        inicio = max(0, corte - overlap)
    return partes


def titulo_da_pagina(texto: str) -> str:
    linhas = [l.strip() for l in texto.splitlines() if l.strip()]
    for linha in linhas[:8]:
        if re.match(r"^\d+(\.\d+)*\.\s+", linha) or "Módulo" in linha or "Login" in linha:
            return linha[:90]
    return linhas[0][:90] if linhas else "Manual CredenciaPE"


@st.cache_data(show_spinner=False)
def carregar_manual() -> Tuple[List[Dict], List[Dict]]:
    with open(MANUAL_JSON, "r", encoding="utf-8") as f:
        paginas = json.load(f)

    chunks = []
    for pagina in paginas:
        page_number = int(pagina["page"])
        text = pagina.get("text", "")
        title = titulo_da_pagina(text)
        for idx, parte in enumerate(quebrar_texto(text), start=1):
            norm = normalizar(parte)
            chunks.append({
                "page": page_number,
                "part": idx,
                "title": title,
                "text": parte,
                "norm": norm,
                "tokens": set(tokens_relevantes(parte)),
            })
    return paginas, chunks


def buscar_no_manual(pergunta: str, chunks: List[Dict], limite: int = 5) -> List[Dict]:
    pergunta_norm = normalizar(pergunta)
    q_tokens = tokens_relevantes(pergunta)
    q_set = set(q_tokens)
    resultados = []

    for chunk in chunks:
        c_norm = chunk["norm"]
        c_tokens = chunk["tokens"]
        inter = q_set.intersection(c_tokens)
        score = 0.0
        score += len(inter) * 5

        for tok in q_set:
            if tok in c_norm:
                score += 1.8

        for frase in [
            "primeiro login", "esqueci senha", "redefinir senha", "cadastrar edital",
            "publicar edital", "suspender edital", "criar ata", "publicar ata",
            "analisar solicitacao", "habilitacao juridica", "habilitacao tecnica",
            "cadastrar cotacao", "acompanhar cotacao", "finalizar cotacao",
            "ordem fornecimento", "assinar documento", "fluxo assinatura",
            "cadastrar fornecedor", "cadastrar itens", "relatorio pesquisa",
        ]:
            if frase in pergunta_norm and frase in c_norm:
                score += 16

        if pergunta_norm and pergunta_norm in c_norm:
            score += 30

        if score > 0:
            item = dict(chunk)
            item["score"] = score
            resultados.append(item)

    resultados.sort(key=lambda x: x["score"], reverse=True)

    escolhidos = []
    paginas_usadas = set()
    for r in resultados:
        if r["page"] not in paginas_usadas or len(escolhidos) < 2:
            escolhidos.append(r)
            paginas_usadas.add(r["page"])
        if len(escolhidos) >= limite:
            break

    if not escolhidos and chunks:
        escolhidos = chunks[:2]
    return escolhidos


def montar_contexto(contextos: List[Dict], max_chars: int = 9000) -> str:
    blocos = []
    total = 0
    for c in contextos:
        bloco = f"[Página {c['page']} - {c['title']}]\n{c['text']}"
        if total + len(bloco) > max_chars:
            break
        blocos.append(bloco)
        total += len(bloco)
    return "\n\n---\n\n".join(blocos)


def obter_config(nome: str, default: str = "") -> str:
    """Lê configuração priorizando o .env do projeto.

    Antes o app lia st.secrets primeiro. Se uma chave antiga estivesse em
    .streamlit/secrets.toml, ela continuava vencendo a chave nova do .env e
    causava erro 401. Agora a ordem é:
    1) .env do projeto
    2) variável de ambiente do sistema
    3) .streamlit/secrets.toml
    """
    env_local = carregar_env_local()
    if env_local.get(nome):
        return env_local[nome]

    if os.getenv(nome, ""):
        return os.getenv(nome, "")

    try:
        valor = st.secrets.get(nome, "")
    except Exception:
        valor = ""

    return valor or default


def origem_config(nome: str) -> str:
    env_local = carregar_env_local()
    if env_local.get(nome):
        return ".env"
    if os.getenv(nome, ""):
        return "variável do sistema"
    try:
        if st.secrets.get(nome, ""):
            return ".streamlit/secrets.toml"
    except Exception:
        pass
    return "não encontrada"


def obter_secret(nome: str, default: str = "") -> str:
    # Mantido por compatibilidade com o restante do arquivo.
    return obter_config(nome, default)


def limpar_chave(valor: str) -> str:
    valor = (valor or "").strip().strip('"').strip("'")
    placeholders = {
        "SUA_CHAVE_AQUI",
        "COLE_SUA_CHAVE_AQUI",
        "",
    }
    if valor in placeholders:
        return ""
    return valor


def obter_chave_openrouter() -> str:
    return limpar_chave(
        obter_config("OPENROUTER_API_KEY")
    )


def origem_chave_openrouter() -> str:
    if limpar_chave(obter_config("OPENROUTER_API_KEY")):
        return origem_config("OPENROUTER_API_KEY")
    return "não encontrada"


def formato_chave_suspeito(api_key: str) -> bool:
    """Detecta tokens OAuth comuns que não devem ser usados como API key."""
    if not api_key:
        return False
    if api_key.startswith("ya29."):
        return True
    return False


def mascarar_chave(api_key: str) -> str:
    if not api_key:
        return "não configurada"
    if len(api_key) <= 10:
        return "configurada"
    return f"{api_key[:6]}...{api_key[-4:]}"


def chamar_openrouter_rest(api_key: str, modelo: str, prompt: str) -> str:
    """Chama a API OpenRouter usando o endpoint compativel com Chat Completions."""
    modelo_limpo = (modelo or "google/gemini-2.5-flash").strip()
    url = "https://openrouter.ai/api/v1/chat/completions"
    payload = {
        "model": modelo_limpo,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "top_p": 0.8,
        "max_tokens": 1400,
    }
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "Assistente CredenciaPE",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detalhe = exc.read().decode("utf-8", errors="ignore")[:600]
        raise RuntimeError(f"erro HTTP OpenRouter {exc.code}: {detalhe}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"sem conexao com a API OpenRouter: {exc.reason}") from exc

    try:
        message = data["choices"][0]["message"]["content"]
        if isinstance(message, list):
            return "".join(part.get("text", "") for part in message if isinstance(part, dict)).strip()
        return str(message).strip()
    except Exception:
        raise RuntimeError(f"resposta OpenRouter inesperada: {str(data)[:600]}")

def responder_com_openrouter(pergunta: str, contextos: List[Dict], modelo: str) -> str:
    api_key = obter_chave_openrouter()
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY não configurada")

    if formato_chave_suspeito(api_key):
        raise RuntimeError(
            "A chave detectada parece ser token OAuth/login, não uma API key do OpenRouter. "
            "Cole no .env a chave copiada no painel do OpenRouter."
        )

    contexto = montar_contexto(contextos)
    prompt = f"""
Você é um assistente virtual institucional do sistema CredenciaPE/GESIG.
Seu papel é ajudar usuários a usar o sistema com base EXCLUSIVAMENTE no manual fornecido.

REGRAS IMPORTANTES:
1. Responda em português do Brasil.
2. Use linguagem clara, educada, simples e direta.
3. Responda apenas com base no CONTEXTO DO MANUAL.
4. Se a resposta não estiver no contexto, diga: "Não encontrei essa informação no manual enviado." Em seguida, peça para o usuário detalhar a dúvida ou consultar o suporte responsável.
5. Não invente prazos, regras, permissões, links, valores, nomes de telas ou procedimentos.
6. Quando houver passo a passo, use lista numerada.
7. Quando útil, cite a página do manual usando o formato: "(Manual, pág. X)".
8. Se a pergunta for confusa, faça uma pergunta curta para entender melhor.

CONTEXTO DO MANUAL:
{contexto}

PERGUNTA DO USUÁRIO:
{pergunta}

RESPOSTA:
""".strip()

    texto = chamar_openrouter_rest(api_key=api_key, modelo=modelo, prompt=prompt)
    if texto:
        return texto
    raise RuntimeError("OpenRouter não retornou texto")

def resposta_local(pergunta: str, contextos: List[Dict]) -> str:
    if not contextos:
        return "Não encontrei essa informação no manual enviado. Tente escrever a dúvida com outras palavras."

    paginas = ", ".join(str(c["page"]) for c in contextos[:3])
    principal = contextos[0]
    texto = principal["text"]

    frases = re.split(r"(?<=[.!?])\s+", texto)
    q_tokens = set(tokens_relevantes(pergunta))
    frases_rank = []
    for f in frases:
        f_norm_tokens = set(tokens_relevantes(f))
        score = len(q_tokens.intersection(f_norm_tokens))
        if score > 0:
            frases_rank.append((score, f.strip()))
    frases_rank.sort(reverse=True, key=lambda x: x[0])
    melhores = [f for _, f in frases_rank[:5] if len(f) > 20]

    if not melhores:
        melhores = frases[:4]

    corpo = "\n".join([f"{i+1}. {f}" for i, f in enumerate(melhores[:5])])
    return (
        "Estou em modo local. Encontrei no manual estes trechos relacionados:\n\n"
        f"{corpo}\n\n"
        f"Fonte: Manual CredenciaPE, pág. {principal['page']}. Páginas relacionadas: {paginas}."
    )


def gerar_resposta(pergunta: str, chunks: List[Dict], usar_ia: bool, modelo: str) -> Tuple[str, List[Dict], bool]:
    contextos = buscar_no_manual(pergunta, chunks)
    if usar_ia:
        try:
            return responder_com_openrouter(pergunta, contextos, modelo), contextos, True
        except Exception as exc:
            return (
                resposta_local(pergunta, contextos)
                + f"\n\nObservação técnica: o OpenRouter não respondeu agora ({exc}).",
                contextos,
                False,
            )
    return resposta_local(pergunta, contextos), contextos, False


paginas, chunks = carregar_manual()

with st.sidebar:
    st.image(str(ASSETS_DIR / "logo_credencia_pe.jpeg"), use_container_width=True)
    st.image(str(ASSETS_DIR / "logo_gesig.jpeg"), use_container_width=True)

    st.markdown("### Configuração")
    openrouter_key = obter_chave_openrouter()
    usar_openrouter = bool(openrouter_key)
    st.toggle(
        "Usar OpenRouter",
        value=usar_openrouter,
        disabled=True,
        help="O OpenRouter fica ativo automaticamente quando há OPENROUTER_API_KEY configurada.",
    )
    modelo = st.text_input("Modelo OpenRouter", value=obter_secret("OPENROUTER_MODEL", "google/gemini-2.5-flash"))

    chave_origem = origem_chave_openrouter()
    if openrouter_key:
        st.success(f"Chave detectada: {mascarar_chave(openrouter_key)}")
        st.caption(f"Origem da chave usada: {chave_origem}")
        if formato_chave_suspeito(openrouter_key):
            st.error("Formato suspeito: parece token OAuth/login. Troque pela chave copiada no painel do OpenRouter.")
        else:
            st.caption("Se ainda cair no modo local, confira internet, créditos/cota do OpenRouter ou modelo informado.")
    else:
        st.warning("Sem chave OpenRouter. O app usa busca local no manual.")
        st.caption("Crie um arquivo .env com OPENROUTER_API_KEY=...")

    with st.expander("Diagnóstico OpenRouter"):
        st.write("`.env` encontrado:", ENV_FILE.exists())
        st.write("Chave configurada:", bool(openrouter_key))
        st.write("Origem da chave:", chave_origem)
        st.write("Formato suspeito:", formato_chave_suspeito(openrouter_key))
        st.write("Modelo:", modelo)
        st.write("Endpoint REST:", "OpenRouter")

    st.markdown("### Manual")
    st.markdown(
        f"<div class='manual-status'>Manual carregado: {len(paginas)} páginas<br>{len(chunks)} blocos de busca</div>",
        unsafe_allow_html=True,
    )

    if MANUAL_PDF.exists():
        with open(MANUAL_PDF, "rb") as f:
            st.download_button(
                "Baixar manual usado pela IA",
                data=f,
                file_name="manual_credenciape.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

    if st.button("Limpar conversa", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown(
    """
    <div class="topbar">
        <div>
            <p class="brand-title">Assistente Virtual CredenciaPE</p>
            <div class="brand-subtitle">Chatbot de apoio ao usuário, respondendo com base no manual oficial do sistema.</div>
        </div>
        <div style="text-align:right;color:#F4F8FF;font-weight:800;">Governo de Pernambuco<br><span style="font-weight:600;color:#A9B8D0;">GESIG</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
        <h1>Como posso ajudar no CredenciaPE?</h1>
        <p>
            Tire dúvidas sobre login, editais, credenciamento, fornecedores, cotação, itens,
            pesquisa e assinatura. As respostas são geradas a partir do manual carregado no sistema.
        </p>
        <div class="pill-row">
            <span class="pill">📘 Baseado no manual</span>
            <span class="pill">🔎 Busca por página</span>
            <span class="pill">🤖 OpenRouter opcional</span>
            <span class="pill">🔵 Interface institucional azul</span>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    <div class="info-card">
        <h3>Atendimento guiado</h3>
        <div class="small-muted">Respostas em formato de passo a passo para ajudar o usuário dentro do sistema.</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div class="info-card">
        <h3>Sem inventar informação</h3>
        <div class="small-muted">Quando a dúvida não está no manual, o assistente informa que não encontrou no documento.</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div class="info-card">
        <h3>Pronto para OpenRouter</h3>
        <div class="small-muted">Lê .env, secrets do Streamlit ou variável do Windows e chama a API via REST.</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.markdown("### Perguntas rápidas")
perguntas_rapidas = [
    "Como faço o primeiro login?",
    "Como redefinir minha senha?",
    "Como cadastrar um edital?",
    "Como publicar um edital?",
    "Como analisar uma solicitação de credenciamento?",
    "Como cadastrar uma cotação?",
    "Como assinar um documento?",
]
cols = st.columns(4)
for i, pergunta_rapida in enumerate(perguntas_rapidas):
    with cols[i % 4]:
        if st.button(pergunta_rapida, key=f"quick_{i}", use_container_width=True):
            st.session_state.pending_question = pergunta_rapida

st.markdown("### Chat")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Olá! Sou o assistente do CredenciaPE. Pergunte algo sobre o uso do sistema e eu responderei com base no manual carregado.",
            "sources": [],
        }
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("Trechos do manual usados na resposta"):
                for fonte in msg["sources"]:
                    trecho = fonte["text"][:700].strip()
                    if len(fonte["text"]) > 700:
                        trecho += "..."
                    st.markdown(
                        f"""
                        <div class="source-box">
                            <span class="source-page">Pág. {fonte['page']}</span><br>
                            <strong>{fonte['title']}</strong><br><br>
                            {trecho}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

pergunta_digitada = st.chat_input("Digite sua dúvida sobre o CredenciaPE...")
pergunta = st.session_state.pop("pending_question", None) or pergunta_digitada

if pergunta:
    st.session_state.messages.append({"role": "user", "content": pergunta, "sources": []})
    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("Consultando o manual..."):
            resposta, fontes, usou_ia = gerar_resposta(pergunta, chunks, usar_openrouter, modelo)
        st.markdown(resposta)
        with st.expander("Trechos do manual usados na resposta"):
            for fonte in fontes:
                trecho = fonte["text"][:700].strip()
                if len(fonte["text"]) > 700:
                    trecho += "..."
                st.markdown(
                    f"""
                    <div class="source-box">
                        <span class="source-page">Pág. {fonte['page']}</span><br>
                        <strong>{fonte['title']}</strong><br><br>
                        {trecho}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.session_state.messages.append({"role": "assistant", "content": resposta, "sources": fontes})

st.markdown(
    """
    <div class="primary-note">
        <strong>Importante:</strong> este chatbot é uma ferramenta de apoio. Para dúvidas oficiais fora do manual,
        encaminhe ao setor responsável pelo CredenciaPE/GESIG.
    </div>
    """,
    unsafe_allow_html=True,
)


