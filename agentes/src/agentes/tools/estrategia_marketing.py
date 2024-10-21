import datetime
import pandas as pd
from pydantic import BaseModel, Field
from typing import Type
from crewai_tools import BaseTool

# Esquema de validação para a ferramenta de estratégia de marketing
class FerramentaEstrategiaMarketingSchema(BaseModel):
    """Esquema de entrada para a Ferramenta de Estratégia de Marketing"""
    name: str = Field(..., description="Nome da ferramenta de estratégia de marketing")
    description: str = Field(..., description="Descrição da ferramenta de estratégia de marketing")
    inventario: str = Field(..., description="Caminho para o arquivo CSV de inventário")
    previsoes_vendas: str = Field(..., description="Caminho para o arquivo CSV de previsões de vendas")

# Ferramenta principal para gerar estratégias de marketing
class FerramentaEstrategiaMarketing(BaseTool):
    name: str = "estrategia_marketing"
    description: str = "Gera estratégias de marketing com base no inventário e previsão de vendas."
    inventario: str = "../data/inventario.csv"
    previsoes_vendas: str = "../data/previsoes_vendas.csv"
    
    # Esquema de argumentos para validação
    args_schema: Type[BaseModel] = FerramentaEstrategiaMarketingSchema

    def _run(self, name: str, description: str, inventario: str, previsoes_vendas: str):
        """
        Gera uma estratégia de marketing com base no inventário e nas previsões de vendas.
        O inventário e as previsões de vendas são carregados a partir de arquivos CSV.
        """
        # Carregar o inventário a partir do CSV
        inventario_df = pd.read_csv(self.inventario)
        
        # Carregar as previsões de vendas a partir do CSV
        previsoes_df = pd.read_csv(self.previsoes_vendas)

        # Criar um dicionário de previsões com base no produto_id para fácil acesso
        previsoes_dict = {row['produto_id']: row['yhat'] for _, row in previsoes_df.iterrows()}

        # Processar os dados do inventário e gerar estratégias
        estrategias = []
        for _, row in inventario_df.iterrows():
            produto_id = row['produto_id']
            quantidade = row['quantidade']
            demanda_prevista = row['predicted_demand']
            data_vencimento = datetime.datetime.strptime(row['data_vencimento'], '%Y-%m-%d')
            dias_para_vencimento = (data_vencimento - datetime.datetime.now()).days
            vendas_previstas = previsoes_dict.get(produto_id, 0)

            # Estratégias para produtos próximos da validade
            if dias_para_vencimento < 30:
                estrategia = self.gerar_prompt_estrategia(
                    produto_id=produto_id,
                    nome_produto=row['nome_produto'],
                    quantidade=quantidade,
                    dias_para_vencimento=dias_para_vencimento,
                    contexto="Produto com menos de 30 dias para vencer. Necessidade de escoar o estoque."
                )
                estrategias.append(estrategia)

            # Estratégias para produtos com estoque alto e baixa demanda
            if quantidade > demanda_prevista:
                estrategia = self.gerar_prompt_estrategia(
                    produto_id=produto_id,
                    nome_produto=row['nome_produto'],
                    quantidade=quantidade,
                    contexto="Estoque alto em relação à demanda prevista."
                )
                estrategias.append(estrategia)

            # Estratégias para vendas previstas menores que a demanda
            if vendas_previstas < demanda_prevista:
                estrategia = self.gerar_prompt_estrategia(
                    produto_id=produto_id,
                    nome_produto=row['nome_produto'],
                    quantidade=quantidade,
                    contexto="Vendas previstas menores que a demanda esperada."
                )
                estrategias.append(estrategia)

        return estrategias

    def gerar_prompt_estrategia(self, produto_id: str, nome_produto: str, quantidade: int, contexto: str, dias_para_vencimento: int = None):
        """
        Função para criar o prompt que será enviado ao modelo de IA, estruturado para gerar estratégias de marketing.
        """
        prompt = f"Produto: {nome_produto} (ID: {produto_id})\n"
        prompt += f"Quantidade em estoque: {quantidade}\n"
        if dias_para_vencimento is not None:
            prompt += f"Dias para vencimento: {dias_para_vencimento}\n"
        prompt += f"Contexto: {contexto}\n"
        prompt += "Crie uma estratégia de marketing para aumentar as vendas deste produto, levando em consideração as informações acima.\n"
        prompt += "A estratégia deve incluir ações promocionais, canais de divulgação e incentivos para os clientes.\n"

        # Simulação de retorno da estratégia gerada pela IA (essa parte seria substituída pela chamada ao modelo de IA)
        estrategia = {
            "produto": nome_produto,
            "estrategia": f"Gerar uma campanha no Instagram e WhatsApp, destacando que há apenas {quantidade} unidades restantes. Oferecer descontos de 20% para vendas rápidas."
        }

        return estrategia

    def _arun(self, inputs: dict):
        raise NotImplementedError("Execução assíncrona não implementada.")
