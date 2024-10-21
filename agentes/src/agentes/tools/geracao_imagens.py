from crewai_tools import BaseTool


class FerramentaGeracaoImagensMarketing(BaseTool):
    name: str = "geracao_imagens_marketing"
    description: str = "Gera imagens publicitárias para campanhas de marketing."

    def _run(self, inputs: dict):
        nome_produto = inputs.get('nome_produto', 'Produto')
        desconto = inputs.get('desconto', '10%')
        plataforma = inputs.get('plataforma', 'Instagram')

        descricao = (f"Crie uma imagem promocional para um desconto de {desconto} em {nome_produto}. "
                     f"A imagem deve ser atrativa e profissional, focada no {desconto} e qualidade do produto.")

        result = dalle.text2im(prompt=descricao, size="1024x1024")

        return result

    def _arun(self, inputs: dict):
        raise NotImplementedError("Execução assíncrona não implementada.")
