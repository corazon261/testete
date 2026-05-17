#from src.services.storage import load_prs_lazy_csv
#from src.core.cleaning import clean_pr_body
from src.services.llm_service import classificar_natureza_pr


def enriquecer_com_ia(registro: dict) -> dict:
    """
    Função pura de transformação.
    Recebe um dicionário imutável e retorna um novo estado enriquecido.
    """
    # Cria uma cópia para manter a imutabilidade estrita do dicionário original
    novo_registro = dict(registro)

    # Obtém a classificação com segurança e custo zero se já estiver em cache
    novo_registro["pr_type"] = classificar_natureza_pr(
        titulo=novo_registro.get("title", ""),
        corpo=novo_registro.get("body", "")
    )

    return novo_registro


#def run_cleaning_pipeline(file_path: str):
    """
    Orquestra o fluxo de dados: Ingestão -> Limpeza.
    Usa map() para garantir processamento lazy.
    """
    raw_stream = load_prs_lazy_csv(file_path)

    cleaned_stream = map(clean_pr_body, raw_stream)

    return cleaned_stream