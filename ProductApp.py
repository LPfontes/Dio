import streamlit as st
import ControlDB
import pandas as pd  
import ImageProcessor as image
class ProductApp:
    def __init__(self):
        st.title("Cadastro de Produto")
        self.product_name = ""
        self.product_price = 0.0
        self.product_description = ""
        self.product_image = None
        self.db = ControlDB.ControlDB()
    def render_product_form(self):
        self.product_name = st.text_input('Nome do Produto')
        self.product_price = st.number_input('Preço do Produto', min_value=0.0, format="%.2f")
        self.product_description = st.text_area('Descrição do Produto')
        self.product_image = st.file_uploader('Imagem do Produto', type=['jpg', 'png', 'jpeg'])

        if st.button('Cadastrar Produto'):
            self.handle_product_submission()

    def handle_product_submission(self):
        if not self.product_name or not self.product_price or not self.product_description or not self.product_image:
            st.error("Por favor, preencha todos os campos.")
        else:
            image_path = f"temp/{self.product_image.name}.webp"
            self.product_image = image.ImageProcessor(self.product_image)
            self.product_image.resize(600, 600)  # Redimensiona a imagem
            self.product_image.resize(150, 150)  # Redimensiona a imagem
            self.product_image.save(image_path)  # Salva a imagem em formato WEBP
            self.product_image = image_path
            # Salva o produto no banco de dados
            if self.db.save_product_to_db(self.product_name, self.product_price, self.product_description, image_path):
                st.success("Produto cadastrado com sucesso!")
                self.render_product_list()
            else:
                st.error("Erro ao cadastrar o produto.")

    def render_product_list(self):
        st.header("Produtos Cadastrados")
        view_mode = st.selectbox("Escolha a forma de visualização:", ["Lista", "Grade"])
        products = self.db.list_products_from_db()
        if not products:
            st.warning("Nenhum produto cadastrado.")
            return

        if view_mode == "Lista":
            # Cria uma lista de dicionários com os dados dos produtos
            # Antes de mostrar a tabela:
            custom_css = """
            <style>
            table {
                width: 100% !important;
                table-layout: fixed;
            }
            th, td {
                word-wrap: break-word;
                text-align: left;
                vertical-align: top;
            }
            img {
                max-width: 100%;
                height: auto;
            }
            </style>
            """
            st.markdown(custom_css, unsafe_allow_html=True)
            product_data = [
                {
                    "Imagem": f'<img src="{product[4]}" width="50">',  # Reduz o tamanho da imagem
                    "Nome": product[1],
                    "Descrição": product[2],
                    "Preço (R$)": f"{product[3]:.2f}"
                }
                for product in products
            ]
            # Converte a lista de dicionários em um DataFrame do pandas
            product_df = pd.DataFrame(product_data)
            # Exibe a tabela no Streamlit com imagens renderizadas como HTML
            st.write(product_df.to_html(escape=False), unsafe_allow_html=True)
        elif view_mode == "Grade":
            cols = st.columns(3)  # Exibe os produtos em 3 colunas
            for index, product in enumerate(products):
                with cols[index % 3]:
                    st.image(product[4], width=50)
                    st.write(f"**Nome:** {product[1]}")
                    st.write(f"**Preço:** R$ {product[3]:.2f}")


