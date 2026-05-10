import os
import json

def cache_exists( path = "data/cache.json" ):
    return os.path.exists(path)

def save_data( data, path = "data/cache.json" ):
    os.makedirs("data" , exist_ok = True)

    with open( path, "w", encoding = "utf-8" ) as files:
        json.dump( data, files, ensure_ascii = False, indent = 2)


def load_data( path="data/cache.json"):
    if not cache_exists(path):
        return None

    with open( path, "r", encoding = "utf-8" ) as files:
        return json.load( files )

# Simulação do pipeline! Pretendemos integrar com o restante do sistema à partir da Semana 2
def fake_pipeline():
    return [
        {"repo": "repo1", "tipo": "bug fix"},
        {"repo": "repo2", "tipo": "feature"}
    ]

def execute_pipeline_using_cache():
    data = load_data()

    if data is not None:
        print( "Usando dados do cache." )
        return data

    print("Precessando dados...")
    data = fake_pipeline()

    save_data( data )
    return data