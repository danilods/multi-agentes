supermercado_ai/
├── README.md                     # Descrição geral do projeto
├── pyproject.toml                # Arquivo de configuração do projeto Python
├── src/                          # Código-fonte do projeto
│   └── supermercado_ai/
│       ├── agents/               # Diretório de agentes
│       │   ├── agente_previsao_demanda.py      # Agente de Previsão de Demanda
│       │   ├── agente_inventario.py            # Agente de Inventário
│       │   ├── agente_marketing.py             # Agente de Marketing
│       │   ├── agente_geracao_imagens.py       # Agente de Geração de Imagens
│       │   └── agente_analise_dados.py         # Agente de Análise de Dados
│       ├── tools/                # Ferramentas utilizadas pelos agentes
│       │   ├── ferramenta_previsao_demanda.py  # Ferramenta de Previsão de Demanda
│       │   ├── ferramenta_analise_inventario.py  # Ferramenta de Análise de Inventário
│       │   ├── ferramenta_estrategia_marketing.py  # Ferramenta de Estratégia de Marketing
│       │   ├── ferramenta_geracao_imagens.py   # Ferramenta de Geração de Imagens Publicitárias
│       │   └── ferramenta_analise_dados.py     # Ferramenta de Análise de Dados
│       ├── main.py               # Arquivo principal para execução do projeto
│       ├── tasks/                # Tasks atribuídas aos agentes
│       │   ├── task_previsao_demanda.yaml      # Task de Previsão de Demanda
│       │   ├── task_inventario.yaml            # Task de Análise de Inventário
│       │   ├── task_marketing.yaml             # Task de Estratégia de Marketing
│       │   ├── task_geracao_imagens.yaml       # Task de Geração de Imagens
│       │   └── task_analise_dados.yaml         # Task de Análise de Dados
│       └── crew.py              # Configuração e orquestração do CrewAI
├── data/                         # Diretório de dados de entrada
│   ├── dados_vendas.csv          # Dados históricos de vendas
│   ├── inventario.csv            # Dados do inventário atual
│   └── previsoes_vendas.csv      # Previsões de vendas (gerado após a execução)
└── resultados/                   # Diretório de resultados
    ├── imagens/                  # Imagens geradas para as campanhas de marketing
    ├── relatorios/               # Relatórios e gráficos gerados
    └── logs/                     # Logs de execução
