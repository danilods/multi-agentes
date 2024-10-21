from crewai import Agent, Task
from tools.ferramenta_previsao import FerramentaRelatorioPrevisao

# Definir o agente
agente_relatorio = Agent(
    role="Analista de Previsão",
    tools=[FerramentaRelatorioPrevisao()],
    goal="Gerar um relatório de previsão de vendas de produtos e categorias.",
    verbose=True
)

# Definir a task
task_relatorio = Task(
    agent=agente_relatorio,
    description="Gerar um relatório com as previsões de vendas dos produtos e categorias.",
    expected_output="Relatório completo em formato Markdown com o Top 10 Produtos e Categorias."
)
