import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pydantic import BaseModel, Field
from typing import Type
from crewai_tools import BaseTool

# Esquema Pydantic para validar os campos de entrada
class AnaliseDadosSchema(BaseModel):
    """Esquema de entrada para DataAnalysisToolMain"""
    name: str = Field(..., description="Nome da ferramenta de análise de dados")
    description: str = Field(..., description="Descrição da ferramenta de análise de dados")
    vendas: str = Field(..., description="Caminho para o arquivo de dados de vendas")
    previsoes: str = Field(..., description="Caminho para o arquivo de previsões de vendas")

# Ferramenta principal de análise de dados
class FerramentaAnaliseDados(BaseTool):
    name: str = "Análise de Dados"
    description: str = "Ferramenta para gerar gráficos e relatórios de BI com base nos dados de vendas e previsões."
    
    # Caminhos padrão para os arquivos
    vendas: str = "../data/dados_vendas.csv"
    previsoes: str = "../resultados/previsoes/previsoes_vendas.csv"
    
    # Esquema de argumentos para validação
    args_schema: Type[BaseModel] = AnaliseDadosSchema

    def _run(self, name: str, description: str, vendas: str, previsoes: str):
        """
        Executa a análise de dados com base nos arquivos de vendas e previsões fornecidos.
        Gera gráficos e relatórios consolidando as informações.
        """
        # Carregar e preparar os dados
        vendas_df = pd.read_csv(self.vendas)
        previsoes_df = pd.read_csv(self.previsoes)

        # Mesclar os dados de vendas e previsões com base no produto_id
        dados_analise = pd.merge(vendas_df, previsoes_df, on="produto_id")

        # Resolver colunas duplicadas: manter a versão correta de 'nome_produto' e 'categoria'
        dados_analise['nome_produto'] = dados_analise['nome_produto_x'].fillna(dados_analise['nome_produto_y'])
        dados_analise['categoria'] = dados_analise['categoria_x'].fillna(dados_analise['categoria_y'])
        
        # Remover as colunas duplicadas desnecessárias
        dados_analise = dados_analise.drop(columns=['nome_produto_x', 'nome_produto_y', 'categoria_x', 'categoria_y'])

        # Preparar as análises por produto e categoria
        receitas = []
        produtos = dados_analise['nome_produto'].unique()
        categorias_agrupadas = {}

        for produto in produtos:
            produto_df = dados_analise[dados_analise['nome_produto'] == produto]
            receita_esperada = produto_df['quantidade_vendida'].sum() * produto_df['yhat'].iloc[0]
            receitas.append(receita_esperada)
            
            # Agrupar por categoria
            categoria = produto_df['categoria'].iloc[0]
            if categoria not in categorias_agrupadas:
                categorias_agrupadas[categoria] = receita_esperada
            else:
                categorias_agrupadas[categoria] += receita_esperada

        # Gerar gráficos de análise e relatório
        self.gerar_graficos(produtos, receitas, categorias_agrupadas)
        self.gerar_relatorio_pdf(produtos, receitas, categorias_agrupadas)

        return "Gráficos e relatório PDF gerados com sucesso."

    def gerar_graficos(self, produtos, receitas, categorias_agrupadas):
        # Gráfico 1: Receita Estimada por Produto
        plt.figure(figsize=(10, 6))
        plt.bar(produtos, receitas, color='blue')
        plt.xlabel('Produto')
        plt.ylabel('Receita Estimada')
        plt.title('Análise de Receitas Estimadas por Produto')
        plt.grid(True)
        plt.savefig('grafico_receitas_por_produto.png')

        # Gráfico 2: Receita Estimada por Categoria
        plt.figure(figsize=(10, 6))
        categorias = list(categorias_agrupadas.keys())
        receitas_por_categoria = list(categorias_agrupadas.values())
        plt.bar(categorias, receitas_por_categoria, color='green')
        plt.xlabel('Categoria')
        plt.ylabel('Receita Estimada')
        plt.title('Análise de Receitas Estimadas por Categoria')
        plt.grid(True)
        plt.savefig('grafico_receitas_por_categoria.png')

    def gerar_relatorio_pdf(self, produtos, receitas, categorias_agrupadas):
        # Gera um relatório consolidado em PDF
        with PdfPages('relatorio_analise.pdf') as pdf:
            # Gráfico de Receita por Produto
            plt.figure(figsize=(10, 6))
            plt.bar(produtos, receitas, color='blue')
            plt.xlabel('Produto')
            plt.ylabel('Receita Estimada')
            plt.title('Análise de Receitas Estimadas por Produto')
            plt.grid(True)
            pdf.savefig()  # Salva o gráfico no PDF
            plt.close()

            # Gráfico de Receita por Categoria
            plt.figure(figsize=(10, 6))
            categorias = list(categorias_agrupadas.keys())
            receitas_por_categoria = list(categorias_agrupadas.values())
            plt.bar(categorias, receitas_por_categoria, color='green')
            plt.xlabel('Categoria')
            plt.ylabel('Receita Estimada')
            plt.title('Análise de Receitas Estimadas por Categoria')
            plt.grid(True)
            pdf.savefig()  # Salva o gráfico no PDF
            plt.close()

            # Adicionar outras informações no PDF (resumo dos dados)
            plt.figure(figsize=(8, 6))
            plt.text(0.1, 0.8, 'Relatório de Análise de Dados', fontsize=18, ha='left')
            plt.text(0.1, 0.6, f'Total de Produtos Analisados: {len(produtos)}', fontsize=12, ha='left')
            plt.text(0.1, 0.5, f'Receita Estimada Total: R$ {sum(receitas):,.2f}', fontsize=12, ha='left')
            plt.text(0.1, 0.4, 'Categorias Analisadas:', fontsize=12, ha='left')
            for i, (categoria, receita) in enumerate(categorias_agrupadas.items()):
                plt.text(0.1, 0.3 - i * 0.05, f'  - {categoria}: R$ {receita:,.2f}', fontsize=10, ha='left')
            plt.axis('off')  # Remove eixos do texto
            pdf.savefig()
            plt.close()

    def _arun(self, inputs: dict):
        raise NotImplementedError("Execução assíncrona não implementada.")
