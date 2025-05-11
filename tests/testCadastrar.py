import random
import sys
import os
import requests
from io import BytesIO
from PIL import Image

# Adiciona o caminho da pasta ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Agora você pode importar o módulo
import ControlDB as db

def baixar_imagem(url, caminho_destino):
    """
    Faz o download de uma imagem a partir de uma URL e salva localmente.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.save(caminho_destino)
            print(f"Imagem salva em: {caminho_destino}")
            return caminho_destino
        else:
            print(f"Erro ao baixar a imagem. Código HTTP: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erro ao baixar a imagem: {e}")
        return None

def cadastrar_produtos_teste(db):
    nomes = ["Produto A", "Produto B", "Produto C", "Produto D", "Produto E"]
    descricoes = [
        "Descrição curta do produto.",
        "Produto de excelente qualidade.",
        "Mais vendido da categoria.",
        "Produto com garantia estendida.",
        "Novo lançamento."
    ]
    imagem_url_exemplo = "https://stadiolab01.blob.core.windows.net/fotos/3e0fc55c-1dac-443e-a899-37896a3c52e8_placeholder.webp"
    caminho_imagem_local = "temp/placeholder.webp"

    # Baixa a imagem do exemplo e salva localmente
    if not os.path.exists("temp"):
        os.makedirs("temp")
    imagem_local = baixar_imagem(imagem_url_exemplo, caminho_imagem_local)

    if not imagem_local:
        print("Erro ao baixar a imagem. Cadastro abortado.")
        return

    for i in range(20):
        nome = f"{random.choice(nomes)} {i+1}"
        descricao = random.choice(descricoes)
        preco = random.uniform(10.0, 200.0)
        db.save_product_to_db(name=nome, price=preco, description=descricao, image=imagem_local)

    print("20 produtos cadastrados com sucesso.")

if __name__ == "__main__":
    # Inicializa o banco de dados
    db = db.ControlDB()
    # Cadastra produtos de teste
    cadastrar_produtos_teste(db)
