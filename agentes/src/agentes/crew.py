import os
from crewai import Agent, Task, Crew, Process
from langchain.agents import Tool
from tools.custom_tool import PredictToolMain
from tools.geracao_imagens import FerramentaGeracaoImagensMarketing
from tools.analise_inventario import FerramentaAnaliseInventario
from tools.estrategia_marketing import FerramentaEstrategiaMarketing
from tools.analise_dados import FerramentaAnaliseDados


os.environ["OPENAI_API_KEY"] = ""
predict = PredictToolMain()

# Criar o agente de treinamento
training_agent = Agent(
    role='Agente de Treinamento de Modelo',
    goal='Treinar e salvar o modelo de previsão de vendas',
    verbose=True,
    memory=False,
    tools=[predict],  # Passar a tool diretamente

    backstory=""" Você é um especialista em aprendizado de máquina, dedicado a garantir que o modelo de previsão de vendas da empresa seja o mais preciso possível.
    Seu trabalho incansável envolve a análise constante de grandes volumes de dados históricos e atuais de vendas. Você tem uma habilidade única para 
    ajustar modelos de machine learning e otimizar suas configurações para prever com precisão as tendências de venda futuras."""
)

# Criar a task de treinamento
train_model_task = Task(
    description='Treinar o modelo de previsão de vendas e salvar no diretório de modelos.',
    expected_output="""Relatório com a lista dos top 10 produdos que possuem maior probabilidade de venda e o modelo treinado salvo no diretório de modelos. 
    Relatório com a lista das 10 categorias de produtos que tem maior previsão de venda no mês.""",
    output_file="../resultados/previsao_vendas.md",
    agent=training_agent
)

# Agente de Inventário
inventory_agent = Agent(
    role='Gerente de Inventário',
    goal='Analisar o inventário e prever necessidades de reposição.',
    verbose=True,
    tools=[FerramentaAnaliseInventario()],
    backstory="""
    Como Gerente de Inventário, você é o guardião das prateleiras da empresa. Com um olhar atento, você monitora 
    de perto o estoque e garante que produtos essenciais nunca estejam em falta. Sua experiência garante que a 
    empresa maximize sua eficiência, evitando desperdícios e garantindo que as prateleiras estejam sempre 
    abastecidas com os produtos mais importantes.
    
    """
)

# Task de Análise de Inventário
inventory_task = Task(
    description="Analisar os dados de inventário e prever as necessidades de reposição com base nas previsões de vendas.",
    expected_output="""Um relatório com recomendações de produtos que precisam ser reabastecidos. A lista deve conter as informações detalhadas do produto:
        nome_produto: <nome do produto>
        disponibilidade_atual: <informação da disponibilidade atual>
        demanda_prevista: <informação sobre a previsão de compra do produto>
        """,
    output_file="../resultados/relatorio_inventario.md",
    agent=inventory_agent
)

# Agente de Marketing
marketing_agent = Agent(
    role='Especialista em Marketing',
    goal='Criar estratégias de marketing para impulsionar vendas de produtos.',
    verbose=True,
    tools=[FerramentaEstrategiaMarketing()],
    backstory="""
    Você é um estrategista de marketing talentoso, conhecido por sua habilidade em criar campanhas que capturam a 
    atenção do público. Com uma vasta experiência em campanhas digitais e marketing de produto, você é responsável 
    por garantir que os produtos certos sejam promovidos no momento certo, atingindo o público-alvo de forma 
    eficaz. Sua criatividade e visão estratégica ajudam a empresa a aumentar as vendas e a atrair novos clientes."""
)

# Task de Estratégia de Marketing
marketing_task = Task(
    description="Desenvolver estratégias de marketing com base nas previsões de vendas.",
    expected_output="""
        Um plano de marketing com campanhas estratégicas de publicidade.
        1. Campanha de Lançamento: <Descrição da campanha de lançamento>
        2. Campanha de Destaque do Produto: <Descrição da campanha de destaque do produto>
        3. Campanha de Influenciadores: <Descrição da campanha de influenciadores>
        4. Campanha de Email: <Descrição da campanha de email>
        5. Campanha de Mídia Social: <Descrição da campanha de mídia social>
    """,
    output_file="../resultados/relatorio_marketing.md",
    agent=marketing_agent
)

# # Agente de Geração de Imagens
# image_generation_agent = Agent(
#     role='Designer de Marketing',
#     goal='Gerar imagens publicitárias para campanhas de marketing.',
#     verbose=True,
#     tools=[FerramentaGeracaoImagensMarketing()],
#     backstory="""
#     Você é um designer de marketing visual renomado, especializado em criar imagens que capturam a essência de um 
#     produto e seu apelo ao público. Com uma vasta experiência em design gráfico e marketing digital, você garante 
#     que cada imagem criada para campanhas publicitárias seja visualmente impactante, atraente e alinhada à 
#     estratégia da marca."""
# )

# # Task de Geração de Imagens para Marketing
# image_generation_task = Task(
#     description="Criar imagens publicitárias baseadas nas campanhas de marketing desenvolvidas.",
#     expected_output="Um conjunto de imagens publicitárias para as campanhas.",
#     output_file="/resultados/imagens_publicitarias.jpgs",
#     agent=image_generation_agent
# )

# Agente de Análise de Dados
data_analysis_agent = Agent(
    role='Analista de Dados',
    goal='Gerar gráficos e relatórios estratégicos para a diretoria.',
    verbose=True,
    tools=[FerramentaAnaliseDados()],
    backstory="""
    Como Analista de Dados, você é o cérebro por trás das decisões estratégicas da empresa. Com uma mente lógica e 
    orientada por dados, você gera relatórios detalhados e gráficos que fornecem ao comitê diretor uma visão clara 
    e precisa do desempenho da empresa. Seu trabalho é essencial para que a diretoria tome decisões informadas e 
    direcionadas ao crescimento contínuo e sustentável."""
)

# Task de Análise de Dados
data_analysis_task = Task(
    description="Gerar gráficos e relatórios estratégicos para a diretoria.",
    expected_output="Um relatório com gráficos que resumam as principais métricas de desempenho.",
    output_file="../resultados/relatorio_diretoria.pdf",
    agent=data_analysis_agent
)

# Criar a crew
equipe = Crew(
    agents=[training_agent, inventory_agent, marketing_agent, data_analysis_agent],
    tasks=[train_model_task, inventory_task, marketing_task, data_analysis_task],
    process=Process.sequential  # ou outro processo, como parallel
)

# Executar o processo com os inputs
equipe.kickoff()
