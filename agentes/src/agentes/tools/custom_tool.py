from crewai_tools import BaseTool
from typing import Dict, List, Type
from pydantic.v1 import BaseModel, Field
from prophet import Prophet

import pandas as pd
import os

class PredictTool(BaseModel):
    """Esquema de entrada para PredictToolMain"""
    name: str = Field(..., description="Nome da ferramenta de previsão")
    description: str = Field(..., description="Descrição da ferramenta de previsão")
    vendas: str = Field(..., description="Caminho de destino do CSV de vendas")
    historico: str = Field(..., description="Caminho do CSV histórico de vendas")

class PredictToolMain(BaseTool):
    name: str = "Previsão de Vendas"
    description: str = "Modelo para previsão de vendas mensal de um produto."
    
    # Caminhos padrão
    vendas: str = "../data/dados_vendas.csv"
    historico: str = "../data/historico_vendas.csv"
    
    args_schema: Type[BaseModel] = PredictTool
    
    def _run(self, name: str, description: str, vendas: str, historico: str):
        """
        Executa o modelo de previsão de vendas, unindo os dados de vendas atuais e históricos, e retorna as previsões.
        """
        # Carregar e preparar os dados
        vendas_df = pd.read_csv(self.vendas)
        historico_df = pd.read_csv(self.historico)
        
        # Combinar os datasets
        dados = pd.concat([vendas_df, historico_df])
        dados['data'] = pd.to_datetime(dados['data'])

        # Agrupar as vendas mensais por produto
        dados_mensais = dados.groupby([pd.Grouper(key='data', freq='M'), 'produto_id', 'nome_produto', 'categoria']).agg({
            'quantidade_vendida': 'sum'
        }).reset_index()

        previsoes = []
        for produto_id in dados_mensais['produto_id'].unique():
            df_produto = dados_mensais[dados_mensais['produto_id'] == produto_id].copy()
            df_produto.rename(columns={'data': 'ds', 'quantidade_vendida': 'y'}, inplace=True)
            
            # Verificar se há dados suficientes para o Prophet (mínimo de 6 observações)
            if len(df_produto) < 6:
                continue
            
            # Treinar o modelo Prophet
            modelo = Prophet()
            modelo.fit(df_produto)
            
            # Previsão para o próximo mês
            futuro = modelo.make_future_dataframe(periods=1, freq='M')
            previsao = modelo.predict(futuro)
            
            # Extração dos valores previstos e atributos do produto
            previsao_mes_seguinte = previsao[['ds', 'yhat']].iloc[-1].to_dict()  # Previsão para o próximo mês
            previsao_mes_seguinte['produto_id'] = produto_id
            previsao_mes_seguinte['nome_produto'] = df_produto['nome_produto'].iloc[0]
            previsao_mes_seguinte['categoria'] = df_produto['categoria'].iloc[0]
            
            # Adiciona todas as colunas esperadas no DataFrame
            previsoes.append(previsao_mes_seguinte)

        # Converter previsões para DataFrame e garantir que todas as colunas estejam incluídas
        previsoes_df = pd.DataFrame(previsoes, columns=['ds', 'yhat', 'produto_id', 'nome_produto', 'categoria'])
        
        # Salvar previsões completas em um arquivo CSV
        previsoes_df.to_csv('../resultados/previsoes/previsoes_vendas.csv', index=False)

        # Calcular o Top 5 produtos e categorias
        top_produtos = previsoes_df.groupby(['produto_id', 'nome_produto']).agg({
            'yhat': 'sum'
        }).reset_index().sort_values(by='yhat', ascending=False).head(10)
        top_produtos.to_csv('../resultados/previsoes/top_10_produtos.csv', index=False)

        top_categorias = previsoes_df.groupby('categoria').agg({
            'yhat': 'sum'
        }).reset_index().sort_values(by='yhat', ascending=False).head(10) 
        top_categorias.to_csv('../resultados/previsoes/top_10_categorias.csv', index=False)

        # Gerar o relatório em Markdown
        markdown_relatorio = self.gerar_relatorio_markdown(top_produtos, top_categorias)
        return markdown_relatorio

    def gerar_relatorio_markdown(self, top_produtos, top_categorias):
        # Gerar o conteúdo do relatório
        markdown = "# Relatório de Previsão de Vendas para o Próximo Mês\n\n"
        markdown += "## Top 5 Produtos que podem ser mais vendidos:\n"
        for i, row in top_produtos.iterrows():
            markdown += f"{i+1}. **{row['nome_produto']}** - Previsão de vendas: {row['yhat']:.2f} unidades\n"

        markdown += "\n## Top 5 Categorias que podem ser mais vendidas:\n"
        for i, row in top_categorias.iterrows():
            markdown += f"{i+1}. **{row['categoria']}** - Previsão de vendas: {row['yhat']:.2f} unidades\n"

        markdown += "\n_Gerado automaticamente pela ferramenta de previsão de vendas._\n"
        return markdown
