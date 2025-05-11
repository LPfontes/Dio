from azure.storage.blob import BlobServiceClient
import os
import pymssql
import uuid
from dotenv import load_dotenv

class ControlDB:
    def __init__(self):
        load_dotenv()
        self.blob_connection_string = os.getenv("BLOB_CONNECTION_STRING")
        self.blob_container_name = os.getenv("BLOB_CONTAINER_NAME")
        self.blob_account_name = os.getenv("BLOB_ACCOUNT_NAME")
        
        self.sql_server = os.getenv("SQL_SERVER")
        self.sql_database = os.getenv("SQL_DATABASE")
        self.sql_user = os.getenv("SQL_USER")
        self.sql_password = os.getenv("SQL_PASSWORD")

    def upload_blob(self, file_path):
        try:
            blob_service_client = BlobServiceClient.from_connection_string(self.blob_connection_string)
            container_client = blob_service_client.get_container_client(self.blob_container_name)
            
            file_name = file_path.split('/')[-1]
            blob_name = f"{uuid.uuid4()}_{file_name}"
            blob_client = container_client.get_blob_client(blob_name)
            
            with open(file_path, "rb") as file:
                blob_client.upload_blob(file, overwrite=True)
            
            return f"https://{self.blob_account_name}.blob.core.windows.net/{self.blob_container_name}/{blob_name}"
        except Exception as e:
            print(f"Erro ao fazer upload do blob: {e}")
            return None

    def save_product_to_db(self, name, price, description, image):
        try:
            image_url = self.upload_blob(image)
            if not image_url:
                return False
            
            conn = pymssql.connect(server=self.sql_server, user=self.sql_user, password=self.sql_password, database=self.sql_database)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Produtos (nome, descricao, preco, imagem_url) VALUES (%s, %s, %s, %s)",
                (name, description, price, image_url)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao salvar produto no banco de dados: {e}")
            return False
        
    def list_products_from_db(self, page: int = 1, page_size: int = 10):
        try:
            offset = (page - 1) * page_size
            conn = pymssql.connect(
                server=self.sql_server,
                user=self.sql_user,
                password=self.sql_password,
                database=self.sql_database
            )
            cursor = conn.cursor()
            query = f"""
                SELECT * FROM Produtos
                ORDER BY id  
                OFFSET %s ROWS
                FETCH NEXT %s ROWS ONLY;
            """
            cursor.execute(query, (offset, page_size))
            products = cursor.fetchall()
            cursor.close()
            conn.close()
            return products
        except Exception as e:
            print(f"Erro ao listar produtos do banco de dados: {e}")
            return []
    
    def update_product_in_db(self, product_id, name, price, description, image_path=None):
        try:
            conn = pymssql.connect(
                server=self.sql_server,
                user=self.sql_user,
                password=self.sql_password,
                database=self.sql_database
            )
            cursor = conn.cursor()

            if image_path:
                image_url = self.upload_blob(image_path)
                if not image_url:
                    return False
                # Atualiza tudo, incluindo a imagem
                cursor.execute("""
                    UPDATE Produtos 
                    SET nome = %s, descricao = %s, preco = %s, imagem_url = %s
                    WHERE id = %s
                """, (name, description, price, image_url, product_id))
            else:
                # Atualiza sem alterar a imagem
                cursor.execute("""
                    UPDATE Produtos 
                    SET nome = %s, descricao = %s, preco = %s
                    WHERE id = %s
                """, (name, description, price, product_id))

            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao atualizar o produto no banco de dados: {e}")
            return False

    def delete_blob(self, product_id):
        try:
            conn = pymssql.connect(
                server=self.sql_server,
                user=self.sql_user,
                password=self.sql_password,
                database=self.sql_database
            )
            cursor = conn.cursor()

            # Opcional: buscar URL da imagem antes de deletar para também remover do Blob
            cursor.execute("SELECT imagem_url FROM Produtos WHERE id = %s", (product_id,))
            result = cursor.fetchone()
            if result:
                image_url = result[0]
                # Extração do nome do blob da URL
                blob_name = image_url.split("/")[-1]
                blob_service_client = BlobServiceClient.from_connection_string(self.blob_connection_string)
                container_client = blob_service_client.get_container_client(self.blob_container_name)
                blob_client = container_client.get_blob_client(blob_name)
                blob_client.delete_blob()  # Apaga a imagem do Azure Blob Storage
        except Exception as e:
            print(f"Erro ao deletar blob: {e}")
            return False
    def delete_product_from_db(self, product_id):
        # Primeiro, tenta deletar o blob associado ao produto
        self.delete_blob(product_id)
        # Depois, tenta deletar o produto do banco de dados
        try:
            conn = pymssql.connect(
                server=self.sql_server,
                user=self.sql_user,
                password=self.sql_password,
                database=self.sql_database
            )
            cursor = conn.cursor()

            # Apaga o produto do banco
            cursor.execute("DELETE FROM Produtos WHERE id = %s", (product_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao deletar produto: {e}")
            return False
