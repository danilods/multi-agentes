import random
from datetime import datetime, timedelta
import os

# Categorias e produtos
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

# Funções auxiliares para gerar dados aleatórios
def random_vencimento():
    """Gera uma data de vencimento aleatória entre 30 e 365 dias no futuro."""
    return (datetime.now() + timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')

def random_localizacao():
    """Gera uma localização aleatória no supermercado."""
    corredor = random.randint(1, 10)
    prateleira = random.choice(['A', 'B', 'C', 'D'])
    return f"Corredor {corredor}, Prateleira {prateleira}"

def gerar_inventario(num_registros=1000):
    inventario = {}
    id_counter = 1

    # Distribuir os produtos pelas categorias, gerando num_registros no total
    while len(inventario) < num_registros:
        for categoria, produtos in product_names.items():
            for produto in produtos:
                produto_id = f"prod_{id_counter:04d}"
                inventario[produto_id] = {
                    "nome_produto": produto,
                    "categoria": categoria,
                    "quantidade": random.randint(10, 500),  # Quantidade aleatória em estoque
                    "predicted_demand": random.randint(20, 400),  # Demanda prevista
                    "data_vencimento": random_vencimento(),  # Data de vencimento aleatória
                    "localizacao": random_localizacao()  # Localização aleatória
                }
                id_counter += 1
                if len(inventario) >= num_registros:
                    break
            if len(inventario) >= num_registros:
                break

    # Criar o diretório data se não existir
    os.makedirs("data", exist_ok=True)
    
    # Salvar inventário no arquivo CSV
    output_path = os.path.join("data", "inventario.csv")
    with open(output_path, 'w') as f:
        f.write("produto_id,nome_produto,categoria,quantidade,predicted_demand,data_vencimento,localizacao\n")
        for produto_id, dados in inventario.items():
            f.write(f"{produto_id},{dados['nome_produto']},{dados['categoria']},{dados['quantidade']},{dados['predicted_demand']},{dados['data_vencimento']},{dados['localizacao']}\n")

    return inventario, f"Inventário gerado com {num_registros} produtos e salvo em {output_path}"

# Gerar inventário robusto com 1000 produtos
inventario, mensagem = gerar_inventario(num_registros=1000)
print(mensagem)
