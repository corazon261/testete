# 📊 Análise Semântica de Pull Requests - RP-III

Este projeto aplica conceitos de Programação Funcional e Inteligência Artificial para analisar metadados e comentários de Pull Requests do GitHub.

## 👥 Integrantes do Grupo
* **Adriano Barbosa**

## 🏗️ Estrutura do Projeto
```text
ANALISE-PULL-REQUESTS/
├── data/                   
│   └── .gitkeep            
├── src/
│   ├── __init__.py         
│   ├── main.py             
│   ├── core/               
│   │   ├── __init__.py
│   │   ├── aggregation.py
│   │   ├── cleaning.py
│   │   └── processing.py
│   └── services/           
│       ├── __init__.py
│       ├── llm_service.py
│       └── storage.py
├── tests/                  
│   ├── test_cleaning.py
│   └── test_processing.py
├── ui/                     
│   ├── __init__.py
│   ├── components.py
│   └── dashboard.py
├── .env                    
├── .gitignore              
├── README.md               
└── requirements.txt

## 🛠️ Tecnologias e Paradigmas
- **Python 3.10+**
- **Agno (Phidata):** Framework para orquestração de agentes de IA.
- **Paradigma Funcional:** Uso extensivo de Imutabilidade, Funções Puras e Ingestão Lazy (Generators).
- **Streamlit:** Interface de usuário para exibição de dashboards e análise de dados.

## 🏗️ Arquitetura Modular
O projeto segue uma separação rigorosa de responsabilidades:
- `src/core/`: Núcleo da aplicação. Contém apenas funções puras (sem efeitos colaterais) para limpeza e transformação de dados.
- `src/services/`: Camada de infraestrutura. Gerencia a leitura de arquivos (Storage) e a comunicação com agentes de IA (Agno).
- `ui/`: Camada de visualização utilizando componentes Streamlit.
- `data/`: Diretório local para armazenamento do dataset bruto do Kaggle.

## 🚀 Como Configurar e Rodar

### 1. Preparar o Ambiente
Clone o repositório e crie um ambiente virtual:
```bash
git clone [https://github.com/adrianobarbosaaluno-dotcom/AnalisePullRequest.git](https://github.com/adrianobarbosaaluno-dotcom/AnalisePullRequest.git)
cd AnalisePullRequest
python -m venv venv