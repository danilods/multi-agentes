import pandas as pd
from pydantic import BaseModel, Field
from typing import Type
from crewai_tools import BaseTool

# Esquema de validação de entradas para a ferramenta de inventário
class FerramentaAnaliseInventarioSchema(BaseModel):
    """Esquema de entrada para InventoryToolMain"""
    name: str = Field(..., description="Nome da ferramenta de inventário")
    description: str = Field(..., description="Descrição da ferramenta de inventário")
    inventario: str = Field(..., description="Caminho para o arquivo CSV de inventário")

# Ferramenta principal de análise de inventário
class FerramentaAnaliseInventario(BaseTool):
    name: str = "Análise de Inventário"
    description: str = "Ferramenta para análise e previsão de necessidades de reposição de inventário."

    # Caminho padrão para o arquivo de inventário
    inventario: str = "../data/inventario.csv"
    
    # Esquema de argumentos para validação
    args_schema: Type[BaseModel] = FerramentaAnaliseInventarioSchema

    def _run(self, name: str, description: str, inventario: str):
        """
        Executa a análise de inventário com base nos dados do arquivo CSV fornecido.
        Gera um relatório das necessidades de reposição com base na demanda prevista e nos níveis de estoque.
        """
        # Carregar o arquivo de inventário
        inventario_df = pd.read_csv(self.inventario)

        # Verificar se o estoque atual é menor que a demanda prevista
        # Consideramos que a quantidade atual deve ser maior ou igual à demanda prevista (predicted_demand)
        reposicao = inventario_df[inventario_df['quantidade'] < inventario_df['predicted_demand']]

        # Gerar os Top 10 produtos que precisam de reposição urgente
        top_10_reposicao = reposicao.sort_values(by='quantidade').head(10)
        top_10_reposicao.to_csv('../resultados/inventario/top_10_reposicao.csv', index=False)

        # Gerar o relatório em Markdown
        markdown_relatorio = self.gerar_relatorio_markdown(top_10_reposicao)
        
        return markdown_relatorio

    def gerar_relatorio_markdown(self, top_10_reposicao):
        # Gerar o conteúdo do relatório em Markdown
        markdown = "# Relatório de Reposição de Estoque\n\n"
        markdown += "## Top 10 Produtos que precisam de reposição urgente:\n"
        for i, row in top_10_reposicao.iterrows():
            markdown += (f"{i+1}. **{row['nome_produto']}** - Quantidade em estoque: {row['quantidade']} "
                         f"- Demanda prevista: {row['predicted_demand']} - Data de vencimento: {row['data_vencimento']} "
                         f"- Localização: {row['localizacao']}\n")
        
        markdown += "\n_Gerado automaticamente pela ferramenta de análise de inventário._\n"
        return markdown

    def _arun(self, inputs: dict):
        raise NotImplementedError("Execução assíncrona não implementada.")
