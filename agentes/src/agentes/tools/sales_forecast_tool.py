from pydantic import BaseModel, Field
from typing import Any, Type
from crewai_tools import tool
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# Esquema de entrada da tool usando Pydantic
class TrainSalesForecastToolSchema(BaseModel):
    """Esquema de entrada para TrainSalesForecastTool"""
    destination_model_path: str = Field(..., description="Caminho de destino de salvamento do modelo")
    source_path: str = Field(..., description="Caminho de origem dos dados")


@tool
class TrainSalesForecastTool:
    """Tool para treinar o modelo de previsão de vendas"""

    name: str = "Treinar Modelo de Previsão de Vendas"
    description: str = "Tool para treinar e salvar o modelo de previsão de vendas"
    args_schema: Type[BaseModel] = TrainSalesForecastToolSchema  # Esquema de entrada

    def _run(self) -> str:
        """
        Função responsável por treinar o modelo de previsão de vendas e salvar no diretório 'models'.
        """
        source_path = "../data"
        destination_model_path = "../data"
        # Verificar se o diretório de destino existe, se não, criar
        os.makedirs(destination_model_path, exist_ok=True)

        # Carregar os dados de vendas históricos e atuais do caminho de origem
        current_sales = pd.read_csv(f'{source_path}/current_sales.csv')
        historical_sales = pd.read_csv(f'{source_path}/historical_sales_data.csv')

        # Concatenar os dois datasets
        all_sales = pd.concat([current_sales, historical_sales])

        # Converter a coluna 'data' para o formato datetime
        all_sales['data'] = pd.to_datetime(all_sales['data'])

        # Extração de informações de tempo (mês e ano)
        all_sales['mes'] = all_sales['data'].dt.month
        all_sales['ano'] = all_sales['data'].dt.year

        # Criar dummies para variáveis categóricas (produto e categoria)
        all_sales = pd.get_dummies(all_sales, columns=['produto_id', 'nome_produto', 'categoria'], drop_first=True)

        # Definir as variáveis independentes (X) e a variável dependente (y)
        X = all_sales.drop(columns=['quantidade_vendida', 'data'])
        y = all_sales['quantidade_vendida']

        # Dividir os dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Treinar o modelo Random Forest
        model = RandomForestRegressor()
        model.fit(X_train, y_train)

        # Fazer previsões no conjunto de teste
        y_pred = model.predict(X_test)

        # Avaliar o modelo
        mse = mean_squared_error(y_test, y_pred)
        print(f'Mean Squared Error: {mse}')

        # Salvar o modelo treinado no diretório 'models'
        model_path = f'{destination_model_path}/sales_model.pkl'
        joblib.dump(model, model_path)

        return f"Modelo salvo em: {model_path}"
