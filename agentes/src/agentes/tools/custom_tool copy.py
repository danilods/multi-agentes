from crewai_tools import BaseTool
from typing import Dict, List, Type
from pydantic.v1 import BaseModel, Field
import os

class PredictTool(BaseModel):
    """Esquema de entrada para PredictToolMain"""
    name: str = Field(..., description="Exemplo de nome de ferramenta")
    description: str = Field(..., description="Exemplo de descrição da ferramenta")
    destination_model_path: str = Field(..., description="Caminho de destino de salvamento do modelo")
    source_path: str = Field(..., description="Caminho de origem dos dados (pode incluir o nome do arquivo)")

class PredictToolMain(BaseTool):
    name: str = "Previsão de Vendas"
    description: str = "Modelo para previsão de vendas mensal de um produto."
    
    source_path: str = "../data/inventario.csv"
    destination_model_path: str = "../data"

    args_schema: Type[BaseModel] = PredictTool
    
    def _run(self, name: str, description: str, destination_model_path: str, source_path: str) -> str:
        """
        Executa a ferramenta de previsão de vendas.
        """
        # Implementação do processo de previsão de vendas vai aqui
        arquivo = self.ler_arquivo(self.source_path)
        return arquivo

    def ler_arquivo(self, caminho_arquivo):
        """
        Método para leitura de arquivos. Verifica se o caminho já inclui o arquivo.
        """
        try:
            # Verifica se o caminho já é um arquivo
            if not os.path.isfile(caminho_arquivo):
                return f"Arquivo {caminho_arquivo} não encontrado ou não é um arquivo válido."
            
            # Abre o arquivo no modo de leitura
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()
                return conteudo
        except FileNotFoundError:
            return f"Arquivo {caminho_arquivo} não encontrado."
        except Exception as e:
            return f"Erro ao ler o arquivo: {e}"
