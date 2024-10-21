from crewai_tools import BaseTool
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Função para prever vendas usando regressão linear
def prever_vendas(X, y, forecast_period):
    # Dividir os dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treinar o modelo de regressão linear
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    # Prever no conjunto de teste
    y_pred = modelo.predict(X_test)

    # Calcular o erro quadrático médio
    erro = mean_squared_error(y_test, y_pred)
    print(f"Erro quadrado médio da previsão: {erro}")

    # Fazer previsão para o próximo período (exemplo: forecast_period meses)
    previsao_futura = modelo.predict([[len(X) + forecast_period]])
    
    return previsao_futura, erro

class FerramentaPrevisaoDemanda(BaseTool):
    name: str = "previsao_demanda"
    description: str = "Prevê as vendas futuras com base nos dados históricos."

    def _run(self, inputs: dict):
        # Verificar se os campos obrigatórios estão nos inputs
        if 'product_id' not in inputs or 'historical_sales_data' not in inputs or 'forecast_period' not in inputs:
            raise ValueError("Os campos 'product_id', 'historical_sales_data', e 'forecast_period' são obrigatórios.")

        # Extrair os dados fornecidos
        sales_data = inputs['historical_sales_data']
        forecast_period = inputs['forecast_period']

        # Preparar os dados para a regressão
        X = [[i] for i in range(len(sales_data))]
        y = sales_data

        # Fazer a previsão
        previsao_futura, erro = prever_vendas(X, y, forecast_period)

        return {
            "product_id": inputs['product_id'],
            "previsao_futura": previsao_futura[0],  # Previsão de vendas futuras
            "erro": erro
        }

    def _arun(self, inputs: dict):
        raise NotImplementedError("Este agente não suporta execução assíncrona.")
