import random
import sys
import os

# Adiciona o caminho da pasta ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Agora você pode importar o módulo
import ControlDB as db

def cadastrar_produtos_teste(db):
    nomes = ["Produto A", "Produto B", "Produto C", "Produto D", "Produto E"]
    descricoes = [
        "Descrição curta do produto.",
        "Produto de excelente qualidade.",
        "Mais vendido da categoria.",
        "Produto com garantia estendida.",
        "Novo lançamento."
    ]
    imagem_url_exemplo = "https://stadiolab01.blob.core.windows.net/fotos/3d54319b-a3dd-4d56-90b2-64bb9da8bff8_Placeholder.webp"

    for i in range(20):
        nome = f"{random.choice(nomes)} {i+1}"
        descricao = random.choice(descricoes)
        preco = round(random.uniform(10.0, 200.0), 2)
        db.save_product_to_db(nome, descricao, preco, imagem_url_exemplo)

    print("20 produtos cadastrados com sucesso.")
if __name__ == "__main__":
    # Inicializa o banco de dados
    db = db.ControlDB()
    # Cadastra produtos de teste
    cadastrar_produtos_teste(db)
