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
    date_range = pd.date_range(start=start_date, end=end_date)
    
    # Gerar informações dos produtos
    product_info = generate_product_info(num_products)
    
    # Listas para armazenar os dados
    sales_data = []

    # Gerar vendas aleatórias para preencher o total de registros desejado
    for _ in range(total_sales_records):
        date = random.choice(date_range)
        product_id, info = random.choice(list(product_info.items()))
        quantidade_vendida = random.randint(1, 100)  # Quantidade de vendas por registro

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

# Função para converter os dados de vendas no formato esperado pela ferramenta de previsão
def convert_to_tool_format(sales_df):
    # Agrupar por produto e coletar as vendas em uma lista
    product_sales = sales_df.groupby('produto_id')['quantidade_vendida'].apply(list).reset_index()

    # Converter para o formato esperado pela ferramenta
    historical_sales_data = []
    for index, row in product_sales.iterrows():
        historical_sales_data.append({
            "product_id": row['produto_id'],
            "sales": row['quantidade_vendida']
        })
    
    return {"historical_sales_data": historical_sales_data}

# Definir parâmetros
start_date = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')  # Início nos últimos 6 meses
end_date = datetime.now().strftime('%Y-%m-%d')  # Data final é hoje
num_products = 50           # Número de produtos
total_sales_records = 12000  # Total de registros de vendas (12 mil)

# Gerar os dados de vendas
sales_df = generate_sales_data(start_date, end_date, num_products, total_sales_records)

# Converter os dados para o formato esperado pela ferramenta de previsão
historical_sales_data = convert_to_tool_format(sales_df)

# Exibir o resultado
print(historical_sales_data)

# Salvar os dados simulados no formato CSV (opcional)
sales_df.to_csv('sales_data_12000_registros.csv', index=False)
