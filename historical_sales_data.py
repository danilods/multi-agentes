import pandas as pd
import random
from datetime import datetime, timedelta

# Função para gerar nomes e categorias fictícios para os produtos
def generate_product_info(num_products):
    product_names = {
        "Higiene": ["Sabonete", "Shampoo", "Condicionador", "Creme Dental", "Sabonete Líquido", "Desodorante", "Fio Dental"],
        "Limpeza": ["Detergente", "Sabão em Pó", "Amaciante", "Desinfetante", "Multiuso", "Esponja de Aço", "Limpa Vidros"],
        "Alimentação": ["Arroz", "Feijão", "Macarrão", "Açúcar", "Café", "Farinha de Trigo", "Azeite de Oliva"],
        "Bebidas": ["Refrigerante", "Suco de Laranja", "Água Mineral", "Cerveja", "Vinho Tinto", "Vodka", "Energético"],
        "Diversos": ["Pilhas", "Lâmpada", "Carvão para Churrasco", "Papel Alumínio", "Papel Filme", "Fósforo", "Guardanapos"],
        "Cosméticos": ["Batom", "Esmalte", "Loção Hidratante", "Perfume", "Base", "Protetor Solar", "Removedor de Maquiagem"],
        "Frios e Laticínios": ["Queijo Mussarela", "Presunto", "Leite Integral", "Manteiga", "Iogurte", "Queijo Parmesão", "Requeijão"],
        "Carnes": ["Carne Moída", "Frango", "Linguiça", "Picanha", "Costela", "Filé de Peito de Frango", "Bife de Alcatra"],
        "Padaria": ["Pão Francês", "Pão de Forma", "Bolo de Chocolate", "Croissant", "Torta de Frango", "Pão Integral", "Biscoito"],
        "Congelados": ["Pizza Congelada", "Lasanha Congelada", "Batata Frita Congelada", "Hambúrguer Congelado", "Peixe Congelado", "Nuggets", "Sorvete"]
    }
    
    # Lista de categorias disponíveis
    categorias = list(product_names.keys())
    
    product_info = {}
    for i in range(1, num_products + 1):
        categoria = random.choice(categorias)
        nome_produto = random.choice(product_names[categoria])
        product_id = f"prod_{str(i).zfill(3)}"
        preco_unitario = round(random.uniform(5.0, 50.0), 2)
        product_info[product_id] = {
            "nome_produto": nome_produto,
            "categoria": categoria,
            "preco_unitario": preco_unitario
        }
    
    return product_info

# Função para gerar dados fictícios de vendas
def generate_sales_data(start_date, end_date, num_products, total_sales_records):
    # Datas de vendas
    date_range = pd.date_range(start=start_date, end=end_date, freq='M')
    
    # Gerar informações dos produtos
    product_info = generate_product_info(num_products)
    
    # Listas para armazenar os dados
    sales_data = []

    # Gerar vendas aleatórias para preencher o total de registros desejado
    for product_id, info in product_info.items():
        for date in date_range:
            quantidade_vendida = random.randint(50, 500)  # Quantidade de vendas por mês
            sales_data.append([
                date, 
                product_id, 
                info["nome_produto"], 
                info["categoria"], 
                quantidade_vendida, 
                info["preco_unitario"]
            ])
    
    # Converter em DataFrame do pandas
    sales_df = pd.DataFrame(sales_data, columns=[
        'data', 'produto_id', 'nome_produto', 'categoria', 'quantidade_vendida', 'preco_unitario'
    ])
    
    return sales_df

# Definir parâmetros
start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')  # Início nos últimos 12 meses
end_date = datetime.now().strftime('%Y-%m-%d')  # Data final é hoje
num_products = 50           # Número de produtos

# Gerar os dados
sales_df = generate_sales_data(start_date, end_date, num_products, total_sales_records=12000)

# Salvar os dados em um arquivo CSV
sales_df.to_csv('historical_sales_data.csv', index=False)

print("Arquivo 'historical_sales_data.csv' gerado com sucesso!")
