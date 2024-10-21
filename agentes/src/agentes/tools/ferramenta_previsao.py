import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from crewai_tools import BaseTool

import os

# Função para prever vendas usando regressão linear
def prever_vendas(X, y, forecast_period=3):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    erro = mean_squared_error(y_test, y_pred)
    proximo_periodo = len(X) + forecast_period
    previsao_futura = modelo.predict([[proximo_periodo]])[0]
    return previsao_futura, erro

# Função para preparar dados para cada produto
def preparar_dados_produto(df, produto_id):
    produto_df = df[df['produto_id'] == produto_id]
    produto_df['meses_venda'] = (produto_df['data'] - produto_df['data'].min()).dt.days / 30
    X = produto_df[['meses_venda']]
    y = produto_df['quantidade_vendida']
    return X, y

# Função para preparar dados para cada categoria
def preparar_dados_categoria(df, categoria):
    categoria_df = df[df['categoria'] == categoria]
    vendas_agrupadas = categoria_df.groupby('data')['quantidade_vendida'].sum().reset_index()
    vendas_agrupadas['meses_venda'] = (vendas_agrupadas['data'] - vendas_agrupadas['data'].min()).dt.days / 30
    X = vendas_agrupadas[['meses_venda']]
    y = vendas_agrupadas['quantidade_vendida']
    return X, y

# Função para gerar relatório de previsão de vendas
def gerar_relatorio_previsoes(df, forecast_period=3):
    # Prever vendas para todos os produtos
    previsoes_produtos = {}
    for produto_id in df['produto_id'].unique():
        X, y = preparar_dados_produto(df, produto_id)
        if len(X) >= 2:  # Verifica se há dados suficientes
            previsao, erro = prever_vendas(X, y, forecast_period)
            previsoes_produtos[produto_id] = previsao

    # Prever vendas para todas as categorias
    previsoes_categorias = {}
    for categoria in df['categoria'].unique():
        X, y = preparar_dados_categoria(df, categoria)
        if len(X) >= 2:  # Verifica se há dados suficientes
            previsao, erro = prever_vendas(X, y, forecast_period)
            previsoes_categorias[categoria] = previsao

    # Top 10 Produtos e Categorias
    top_10_produtos = sorted(previsoes_produtos.items(), key=lambda x: x[1], reverse=True)[:10]
    top_10_categorias = sorted(previsoes_categorias.items(), key=lambda x: x[1], reverse=True)[:10]

    # Gerar o conteúdo do relatório
    relatorio = {
        "top_10_produtos": top_10_produtos,
        "top_10_categorias": top_10_categorias
    }
    
    return relatorio

# Função para salvar o relatório em Markdown
def salvar_relatorio_em_markdown(relatorio, caminho_arquivo, df):
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    
    with open(caminho_arquivo, 'w', encoding='utf-8') as file:
        file.write("# Relatório de Previsão de Vendas\n")
        file.write("Este relatório contém as previsões de vendas dos **Top 10 Produtos** e **Top 10 Categorias** com base no histórico de vendas.\n\n")

        # Detalhes do Top 10 Produtos
        file.write("## Top 10 Produtos com Maiores Previsões de Vendas\n")
        file.write("| Produto ID | Nome do Produto | Categoria | Previsão de Vendas |\n")
        file.write("|------------|-----------------|-----------|--------------------|\n")
        for produto_id, previsao in relatorio['top_10_produtos']:
            nome_produto = df[df['produto_id'] == produto_id]['nome_produto'].iloc[0]
            categoria_produto = df[df['produto_id'] == produto_id]['categoria'].iloc[0]
            file.write(f"| {produto_id} | {nome_produto} | {categoria_produto} | {previsao:.2f} |\n")

        # Detalhes do Top 10 Categorias
        file.write("\n## Top 10 Categorias com Maiores Previsões de Vendas\n")
        file.write("| Categoria | Previsão de Vendas |\n")
        file.write("|-----------|--------------------|\n")
        for categoria, previsao in relatorio['top_10_categorias']:
            file.write(f"| {categoria} | {previsao:.2f} |\n")

        file.write("\n\n> **Nota:** As previsões são baseadas em modelos de regressão linear usando dados históricos de vendas.\n")
        file.write("> Relatório gerado automaticamente.\n")

# Ferramenta de previsão em lote
class FerramentaPrevisaoDemanda(BaseTool):
    name: str = "relatorio_previsao"
    description: str = "Gera um relatório completo com previsões de vendas de produtos e categorias."

    def _run(self, inputs: dict):
        # Verificar se o caminho do CSV está nos inputs
        if 'caminho_csv' not in inputs:
            raise ValueError("O caminho do arquivo CSV de vendas ('caminho_csv') é obrigatório.")

        # Carregar os dados
        df = pd.read_csv(inputs['caminho_csv'], parse_dates=['data'])

        # Gerar o relatório de previsões
        relatorio = gerar_relatorio_previsoes(df)
        
        # Salvar o relatório em Markdown
        caminho_relatorio = inputs.get('caminho_relatorio', 'results/relatorio_previsao.md')
        salvar_relatorio_em_markdown(relatorio, caminho_relatorio, df)
        
        print(f"Relatório gerado e salvo em {caminho_relatorio}.")
        return {"relatorio_markdown": relatorio, "caminho_relatorio": caminho_relatorio}

    def _arun(self, inputs: dict):
        raise NotImplementedError("Este agente não suporta execução assíncrona.")
