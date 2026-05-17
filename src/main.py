import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

def main():
    print("--- Sistema de Análise de PRs Inicializado ---")
    api_key = os.getenv("LLM_API_KEY")
    
    if not api_key:
        print("Aviso: LLM_API_KEY não encontrada no arquivo .env")
    else:
        print("API Key carregada com sucesso!")

if __name__ == "__main__":
    main()