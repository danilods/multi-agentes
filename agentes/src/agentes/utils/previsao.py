import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Função para preparar os dados de vendas por produto
def preparar_dados_vendas_por_produto(sales_df, produto_id):
    produto_vendas = sales_df[sales_df['produto_id'] == produto_id]
    produto_vendas['meses_venda'] = (produto_vendas['data'] - produto_vendas['data'].min()).dt.days / 30
    X = produto_vendas[['meses_venda']]
    y = produto_vendas['quantidade_vendida']
    return X, y

# Função para prever vendas por produto usando Regressão Linear
def prever_vendas_por_produto(sales_df):
    previsoes_produtos = {}
    for produto_id in sales_df['produto_id'].unique():
        X, y = preparar_dados_vendas_por_produto(sales_df, produto_id)
        if len(X) < 2:  # Garantir que haja dados suficientes para treinar o modelo
            continue
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        modelo = LinearRegression()
        modelo.fit(X_train, y_train)
        proximo_mes = X['meses_venda'].max() + 1
        previsao_proximo_mes = modelo.predict([[proximo_mes]])[0]
        previsoes_produtos[produto_id] = previsao_proximo_mes
    return previsoes_produtos

# Função para preparar os dados de vendas por categoria
def preparar_dados_vendas_por_categoria(sales_df, categoria):
    categoria_vendas = sales_df[sales_df['categoria'] == categoria]
    vendas_agrupadas = categoria_vendas.groupby('data')['quantidade_vendida'].sum().reset_index()
    vendas_agrupadas['meses_venda'] = (vendas_agrupadas['data'] - vendas_agrupadas['data'].min()).dt.days / 30
    X = vendas_agrupadas[['meses_venda']]
    y = vendas_agrupadas['quantidade_vendida']
    return X, y

# Função para prever vendas por categoria usando Regressão Linear
def prever_vendas_por_categoria(sales_df):
    previsoes_categorias = {}
    for categoria in sales_df['categoria'].unique():
        X, y = preparar_dados_vendas_por_categoria(sales_df, categoria)
        if len(X) < 2:  # Garantir que haja dados suficientes para treinar o modelo
            continue
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        modelo = LinearRegression()
        modelo.fit(X_train, y_train)
        proximo_mes = X['meses_venda'].max() + 1
        previsao_proximo_mes = modelo.predict([[proximo_mes]])[0]
        previsoes_categorias[categoria] = previsao_proximo_mes
    return previsoes_categorias

import os

# Função para salvar o relatório no diretório especificado
def salvar_relatorio_em_arquivo(conteudo_md, caminho_arquivo):
    # Criar o diretório, se ele não existir
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    
    # Salvar o relatório no arquivo Markdown
    with open(caminho_arquivo, "w", encoding="utf-8") as file:
        file.write(conteudo_md)
    
    print(f"Relatório salvo com sucesso em: {caminho_arquivo}")

# Função para gerar o conteúdo do relatório em formato Markdown
def gerar_conteudo_relatorio_md(relatorio, sales_df):
    conteudo_md = "# Relatório de Previsão de Vendas\n"
    conteudo_md += "Este relatório contém as previsões de vendas dos **Top 10 Produtos** e **Top 10 Categorias** com base no histórico de vendas.\n\n"

    # Detalhes do Top 10 Produtos
    conteudo_md += "## Top 10 Produtos com Maiores Previsões de Vendas\n"
    conteudo_md += "| Produto ID | Nome do Produto | Categoria | Previsão de Vendas |\n"
    conteudo_md += "|------------|-----------------|-----------|--------------------|\n"
    for produto_id, previsao in relatorio['top_10_produtos']:
        nome_produto = sales_df[sales_df['produto_id'] == produto_id]['nome_produto'].iloc[0]
        categoria_produto = sales_df[sales_df['produto_id'] == produto_id]['categoria'].iloc[0]
        conteudo_md += f"| {produto_id} | {nome_produto} | {categoria_produto} | {previsao:.2f} |\n"

    conteudo_md += "\n\n"

    # Detalhes do Top 10 Categorias
    conteudo_md += "## Top 10 Categorias com Maiores Previsões de Vendas\n"
    conteudo_md += "| Categoria | Previsão de Vendas |\n"
    conteudo_md += "|-----------|--------------------|\n"
    for categoria, previsao in relatorio['top_10_categorias']:
        conteudo_md += f"| {categoria} | {previsao:.2f} |\n"

    conteudo_md += "\n\n"
    conteudo_md += "> **Nota:** As previsões são baseadas em modelos de regressão linear usando dados históricos de vendas.\n"
    conteudo_md += "> Relatório gerado automaticamente.\n"

    return conteudo_md

# Função para gerar o relatório de previsões e salvar no arquivo Markdown
def gerar_relatorio_previsoes(sales_df, caminho_arquivo="results/relatorio_previsao.md"):
    print(sales_df)
    # Prever vendas por produto
    previsoes_produtos = prever_vendas_por_produto(sales_df)
    top_10_produtos = sorted(previsoes_produtos.items(), key=lambda x: x[1], reverse=True)[:10]

    # Prever vendas por categoria
    previsoes_categorias = prever_vendas_por_categoria(sales_df)
    top_10_categorias = sorted(previsoes_categorias.items(), key=lambda x: x[1], reverse=True)[:10]

    # Gerar relatório
    relatorio = {
        "top_10_produtos": top_10_produtos,
        "top_10_categorias": top_10_categorias
    }

    # Gerar o conteúdo do relatório em Markdown
    conteudo_md = gerar_conteudo_relatorio_md(relatorio, sales_df)

    # Salvar o relatório no arquivo
    salvar_relatorio_em_arquivo(conteudo_md, caminho_arquivo)

    return conteudo_md

