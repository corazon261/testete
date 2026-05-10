import os
import time
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAILike
from src.services.llm_service import classificar_natureza_pr

# Força o carregamento do .env
load_dotenv()


def testar_conexao_bruta():
    print("--- TESTE 1: Verificando a API Key e Resposta Bruta da IA ---")
    api_key = os.getenv("LLM_API_KEY")

    if not api_key:
        print("❌ ERRO: LLM_API_KEY não encontrada! Verifique o ficheiro .env")
        return False

    print(f"✅ API Key carregada com sucesso (Inicia com: {api_key[:8]}...)")

    agente = Agent(
        model=OpenAILike(
            id="openai/gpt-3.5-turbo",
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
    )

    prompt = """
    Analise o seguinte Pull Request e classifique a natureza da contribuição.
    Você deve responder estritamente com UMA das seguintes opções: Bugfix, Feature, Refatoracao, ou Documentacao.
    Não adicione nenhuma pontuação, explicação ou texto adicional.

    Título do PR: Fix: crash
    Descrição do PR: resolve o crash do sistema.
    Classificação:
    """

    print("A enviar requisição real para o OpenRouter (aguarde)...")
    inicio = time.time()
    try:
        resposta_bruta = agente.run(prompt).content
        fim = time.time()
        print(f"⏱️ Tempo da requisição: {fim - inicio:.2f} segundos")
        print(f"🤖 Resposta EXATA (bruta) da IA: '{resposta_bruta}'")
        return True
    except Exception as e:
        print(f"❌ Erro de conexão com o OpenRouter: {e}")
        return False


def testar_cenarios_e_cache():
    print("\n--- TESTE 2: Testando Múltiplos Cenários e Cache Duplo ---")

    cenarios = [
        ("Fix: Null pointer exception", "Resolve erro fatal no login."),
        ("Feat: Adiciona botão de dark mode", "Implementado suporte a tema escuro."),
        ("Docs: Atualiza README", "Adicionadas instruções do Docker.")
    ]

    for i, (titulo, corpo) in enumerate(cenarios, 1):
        print(f"\nCenário {i}: {titulo}")

        # Primeira chamada (Deve demorar e ir à API)
        inicio1 = time.time()
        res1 = classificar_natureza_pr(titulo, corpo)
        fim1 = time.time()
        print(f"  ➜ 1ª Chamada (Nova)  | Resultado: {res1} | Tempo: {fim1 - inicio1:.2f}s")

        # Segunda chamada (Deve ser 0.00s)
        inicio2 = time.time()
        res2 = classificar_natureza_pr(titulo, corpo)
        fim2 = time.time()
        print(f"  ➜ 2ª Chamada (Cache) | Resultado: {res2} | Tempo: {fim2 - inicio2:.5f}s")


if __name__ == "__main__":
    sucesso = testar_conexao_bruta()
    if sucesso:
        testar_cenarios_e_cache()