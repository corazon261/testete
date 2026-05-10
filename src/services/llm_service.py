import os
import json
import hashlib
from functools import lru_cache
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAILike

load_dotenv()

# Define o caminho do arquivo de cache
CACHE_FILE = "data/llm_cache.json"


def _carregar_cache_disco() -> dict:
    """Carrega o cache do disco de forma segura."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}


def _salvar_cache_disco(cache: dict) -> None:
    """Salva as novas análises no disco."""
    os.makedirs("data", exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


# Inicializa o dicionário de cache carregando o que já existe
_llm_cache = _carregar_cache_disco()


def criar_agente_openrouter() -> Agent:
    """Instancia o agente conectado ao OpenRouter."""
    return Agent(
        model=OpenAILike(
            id="openrouter/free",
            api_key=os.getenv("LLM_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        ),
        description="Você é um engenheiro de software especialista em analisar repositórios e Pull Requests."
    )


@lru_cache(maxsize=2000)
def classificar_natureza_pr(titulo: str, corpo: str) -> str:
    """
    Classifica o PR com Memoização Dupla (Memória + Disco).
    Garante transparência referencial para o pipeline funcional.
    """
    # 1. Gera um identificador único para o texto analisado
    texto_base = f"{titulo}|{corpo}"
    conteudo_hash = hashlib.md5(texto_base.encode('utf-8')).hexdigest()

    # 2. Verifica se a resposta já existe no cache em disco
    if conteudo_hash in _llm_cache:
        return _llm_cache[conteudo_hash]

    # 3. Se não existe, consome a API
    agente = criar_agente_openrouter()
    prompt = f"""
    Analise o seguinte Pull Request e classifique a natureza da contribuição.
    Você deve responder estritamente com UMA das seguintes opções: Bugfix, Feature, Refatoracao, ou Documentacao.
    Não adicione nenhuma pontuação, explicação ou texto adicional.

    Título do PR: {titulo}
    Descrição do PR: {corpo}

    Classificação:
    """

    resposta = agente.run(prompt).content

    # 4. Pós-processamento puramente funcional
    resposta_limpa = resposta.strip().title()
    categorias_validas = ["Bugfix", "Feature", "Refatoracao", "Documentacao"]

    resultado_final = resposta_limpa if resposta_limpa in categorias_validas else "Outro"

    # 5. Salva o novo resultado no cache para não consultar a API novamente
    _llm_cache[conteudo_hash] = resultado_final
    _salvar_cache_disco(_llm_cache)

    return resultado_final


# As demais funções do serviço podem seguir o mesmo padrão de cache
def analisar_sentimento(texto: str) -> str:
    pass


def resumir_pr(titulo: str, corpo: str, comentarios: list[str]) -> str:
    pass