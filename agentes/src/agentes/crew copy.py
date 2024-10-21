import os
import csv
from crewai import Agent, Task, Crew, Process
from tools.ferramenta_previsao import FerramentaPrevisaoDemanda
from tools.analise_inventario import FerramentaAnaliseInventario
from tools.estrategia_marketing import FerramentaEstrategiaMarketing
from tools.geracao_imagens import FerramentaGeracaoImagensMarketing
from tools.analise_dados import FerramentaAnaliseDados

# Configurando chaves de API para o LLM (se necessário)
os.environ["OPENAI_API_KEY"] = "sk-svcacct-E-L7skk-twQhp5aZe2KP9T6uSF-gSCU1kValpEUMkjDpbzGp-Xw-5_UFEYD6fgTY-_gxbWK9dT3BlbkFJ9PmOUV8B5V0RhBPjrcQ8g38bPcV8WmCiWq6CpA6O44uO2OuXFjavKeda-rcQ1n99PoFkGVAGwA"

# Definição dos agentes e tasks
# Agente de Previsão de Demanda
agente_previsao_demanda = Agent(
    role='Analista de Demanda',
    tools=[FerramentaPrevisaoDemanda()],
    goal='Gerar um relatório da previsão de demanda realizada.',
    verbose=True,
    backstory="""
        Você é um analista de demanda experiente, especializado em utilizar dados históricos de vendas para gera relatório de previsão de
        necessidades futuras. Com um histórico de anos trabalhando em grandes redes de varejo, sua precisão ajuda a 
        empresa a se antecipar às necessidades do mercado e garantir que os produtos certos estejam disponíveis nas 
        prateleiras no momento exato.
    """
)

# Agente de Inventário
agente_inventario = Agent(
    role='Gerente de Inventário',
    tools=[FerramentaAnaliseInventario()],
    goal='Analisar o inventário e prever necessidades de reposição.',
    verbose=True,
    backstory="""
        Como Gerente de Inventário, você é o guardião das prateleiras da empresa. Com um olhar atento, você monitora 
        de perto o estoque e garante que produtos essenciais nunca estejam em falta. Sua experiência garante que a 
        empresa maximize sua eficiência, evitando desperdícios e garantindo que as prateleiras estejam sempre 
        abastecidas com os produtos mais importantes.
    """
)

# Agente de Estratégia de Marketing
agente_marketing = Agent(
    role='Especialista em Marketing',
    tools=[FerramentaEstrategiaMarketing()],
    goal='Criar estratégias de marketing para impulsionar vendas de produtos.',
    backstory="""
        Você é um estrategista de marketing talentoso, conhecido por sua habilidade em criar campanhas que capturam a 
        atenção do público. Com uma vasta experiência em campanhas digitais e marketing de produto, você é responsável 
        por garantir que os produtos certos sejam promovidos no momento certo, atingindo o público-alvo de forma 
        eficaz. Sua criatividade e visão estratégica ajudam a empresa a aumentar as vendas e a atrair novos clientes.
    """
)

# Agente de Geração de Imagens para Marketing
agente_imagens = Agent(
    role='Designer de Marketing',
    tools=[FerramentaGeracaoImagensMarketing()],
    goal='Gerar imagens publicitárias para campanhas de marketing.',
    backstory="""
        Você é um designer de marketing visual renomado, especializado em criar imagens que capturam a essência de um 
        produto e seu apelo ao público. Com uma vasta experiência em design gráfico e marketing digital, você garante 
        que cada imagem criada para campanhas publicitárias seja visualmente impactante, atraente e alinhada à 
        estratégia da marca.
    """
)

# Agente de Análise de Dados
agente_dados = Agent(
    role='Analista de Dados',
    tools=[FerramentaAnaliseDados()],
    goal='Gerar gráficos e relatórios estratégicos para a diretoria.',
    backstory="""
        Como Analista de Dados, você é o cérebro por trás das decisões estratégicas da empresa. Com uma mente lógica e 
        orientada por dados, você gera relatórios detalhados e gráficos que fornecem ao comitê diretor uma visão clara 
        e precisa do desempenho da empresa. Seu trabalho é essencial para que a diretoria tome decisões informadas e 
        direcionadas ao crescimento contínuo e sustentável.
    """
)

# Definir as tasks de cada agente
task_previsao = Task(
    agent=agente_previsao_demanda,
    description="Prever a demanda dos produtos com base no histórico de vendas.",
    expected_output="Previsões de demanda geradas."
)

task_inventario = Task(
    agent=agente_inventario,
    description="Analisar o inventário e prever necessidades de reposição.",
    expected_output="Sugestões de reposição e promoções de produtos geradas."
)

task_marketing = Task(
    agent=agente_marketing,
    description="Gerar estratégias de marketing com base no inventário e previsão de vendas.",
    expected_output="Estratégias de marketing criadas."
)

task_imagens = Task(
    agent=agente_imagens,
    description="Gerar imagens publicitárias para campanhas de marketing.",
    expected_output="Imagens geradas para campanhas publicitárias."
)

task_dados = Task(
    agent=agente_dados,
    description="Gerar gráficos e análises estratégicas para o comitê diretor.",
    expected_output="Relatórios e gráficos gerados para a diretoria."
)

# Criar o Crew e definir o fluxo de execução
crew = Crew(
    agents=[agente_previsao_demanda, agente_inventario, agente_marketing, agente_imagens, agente_dados],
    tasks=[task_previsao, task_inventario, task_marketing, task_imagens, task_dados],
    process=Process.sequential,
    verbose=True
)

# Executar o Crew com os dados carregados
inputs = {
    "caminho_csv": "data/historical_sales_data.csv",  # O arquivo CSV gerado com os dados históricos
    "caminho_relatorio": "results/relatorio_previsao.md"  # Caminho para salvar o relatório
}

result = crew.kickoff(inputs=inputs)
print(result)


