from os import path, getenv, remove
from time import sleep
import streamlit as st
import ControlDB
import ImageProcessor as image
from dotenv import load_dotenv
from PIL import Image
import requests
from io import BytesIO

load_dotenv()

class ProductApp:
    def __init__(self):
        # Inicializa o título do aplicativo e configurações iniciais
        st.title("Cadastro de Produto")
        self.db = ControlDB.ControlDB()  # Instância do banco de dados
        self.set_default_session_state()  # Configura os valores padrão do estado
        self.products = []  # Lista de produtos

    def set_default_session_state(self):
        # Define valores padrão para o estado da sessão
        defaults = {
            "product_name": "",
            "product_price": 0.0,
            "product_description": "",
            "product_image": None,
            "editing_product": False,
            "product_page": 1,
            "page_size": 10
        }
        for key, value in defaults.items():
            st.session_state[key] = value

    def setup_form(self):
        # Configura o botão para abrir o formulário de cadastro
        if st.button("Cadastrar Produto"):
            self.set_default_session_state()
            self.render_product_form()

    @st.dialog("Cadastrar/Editar Produto")
    def render_product_form(self):
        # Renderiza o formulário para cadastrar ou editar produtos
        form_title = "Editar Produto" if st.session_state.editing_product else "Cadastrar Produto"
        st.subheader(form_title)

        with st.form(key="product_form"):
            # Campos do formulário
            st.session_state.product_name = st.text_input("Nome do Produto", value=st.session_state.product_name)
            st.session_state.product_price = st.number_input("Preço do Produto", min_value=0.0, format="%.2f", value=st.session_state.product_price)
            st.session_state.product_description = st.text_area("Descrição do Produto", value=st.session_state.product_description)
            st.session_state.product_image = st.file_uploader("Imagem do Produto", type=['jpg', 'jpeg', 'png'])

            submitted = st.form_submit_button(form_title)

            if submitted:
                if st.session_state.editing_product:
                    # Chama a função de edição
                    self.handle_product_edit()
                    self.set_default_session_state()
                    st.rerun()
                else:
                    # Valida os campos obrigatórios antes de cadastrar
                    if not st.session_state.product_name or not st.session_state.product_description or st.session_state.product_price <= 0:
                        st.error("Por favor, preencha os campos obrigatórios: nome, descrição e preço válido.")
                    else:
                        self.handle_product_submission()
                        self.set_default_session_state()
                        st.rerun()

    def handle_product_submission(self):
        # Lida com o cadastro de um novo produto
        name = st.session_state.product_name
        price = st.session_state.product_price
        description = st.session_state.product_description
        image_file = st.session_state.product_image

        image_path = self.process_image(image_file)  # Processa a imagem enviada

        if self.db.save_product_to_db(name, price, description, image_path):
            st.success("Produto cadastrado com sucesso!")
            try:
                # Remove a imagem temporária após o cadastro
                if image_path and path.exists(image_path):
                    remove(image_path)
            except Exception as e:
                st.warning(f"Imagem temporária não pôde ser removida: {e}")
        else:
            st.error("Erro ao cadastrar o produto.")

    def handle_product_edit(self):
        # Lida com a edição de um produto existente
        product_id = st.session_state.product_id
        name = st.session_state.product_name
        price = st.session_state.product_price
        description = st.session_state.product_description
        image_file = st.session_state.product_image

        # Processa a nova imagem, se enviada
        image_path = self.process_image(image_file) if image_file else None

        if self.db.update_product_in_db(product_id, name, price, description, image_path):
            st.success("Produto atualizado com sucesso!")
            sleep(1)
        else:
            st.error("Erro ao atualizar o produto.")

    def process_image(self, uploaded_image):
        # Processa a imagem enviada ou usa um placeholder
        try:
            if uploaded_image:
                # Processa a imagem enviada pelo usuário
                image_name = path.splitext(uploaded_image.name)[0]
                image_path = f"temp/{image_name}.webp"
                img_processor = image.ImageProcessor(uploaded_image)
                img_processor.resize(300, 300)
                img_processor.save(image_path)
                return image_path
            else:
                # Usa o placeholder se nenhuma imagem for enviada
                placeholder_url = getenv("PLACEHOLDER_URL", "")
                if placeholder_url.startswith("http"):
                    response = requests.get(placeholder_url)
                    if response.status_code == 200:
                        img = Image.open(BytesIO(response.content))
                        img = img.resize((300, 300))
                        image_path = "temp/placeholder.webp"
                        img.save(image_path)
                        return image_path
                    else:
                        st.error("Erro ao carregar a imagem do link.")
                        return None
                else:
                    st.error("URL do placeholder inválida.")
                    return None
        except Exception as e:
            st.error(f"Erro ao processar imagem: {e}")
            return None

    def render_product_list(self):
        # Renderiza a lista de produtos cadastrados
        if self.setup_product_list():
            self.display_products()

    def setup_product_list(self):
        # Configura a lista de produtos com paginação
        st.header("Produtos Cadastrados")
        st.session_state.page_size = st.selectbox("Itens por página", [10, 20, 50, 100], index=1)

        self.products = self.db.list_products_from_db(
            page=st.session_state.product_page,
            page_size=st.session_state.page_size
        )

        if not self.products:
            st.warning("Nenhum produto cadastrado nesta página.")
            return False

        # Configura os botões de paginação
        need_pagination = len(self.products) > st.session_state.page_size
        if need_pagination:
            col1, col2, col3 = st.columns([1, 1, 6])
            with col1:
                if st.button("⬅", key="prev_page") and st.session_state.product_page > 1:
                    st.session_state.product_page -= 1
            with col2:
                if st.button("➡", key="next_page"):
                    st.session_state.product_page += 1
            with col3:
                st.markdown(f"**Página {st.session_state.product_page}**")

        return True

    @st.dialog("confirmar exclusão")
    def delete_product(self, product):
        # Confirmação para deletar um produto
        st.subheader("Deletar Produto")
        st.markdown(f"Você tem certeza que deseja deletar o produto: **{product[1]}**?")

        if st.button("Sim"):
            if self.db.delete_product_from_db(product[0]):
                st.success("Produto deletado com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao deletar o produto.")
        elif st.button("Não"):
            st.rerun()

    def prepare_edit(self, product):
        # Prepara o formulário para edição de um produto
        st.session_state.update({
            "product_id": product[0],
            "editing_product": True,
            "product_name": product[1],
            "product_description": product[2],
            "product_price": float(product[3]),
            "product_image": None
        })
        self.render_product_form()

    def display_products(self):
        # Exibe a lista de produtos com opções de editar e deletar
        for product in self.products:
            with st.container():
                cols = st.columns([1, 3, 3, 2, 2, 2])
                with cols[0]:
                    st.image(product[4], width=100)
                with cols[1]:
                    st.markdown(f"**Nome:** {product[1]}")
                with cols[2]:
                    st.markdown(f"**Descrição:** {product[2]}")
                with cols[3]:
                    st.markdown(f"**Preço:** R$ {product[3]:.2f}")
                with cols[4]:
                    if st.button("Deletar", key=f"delete_{product[0]}"):
                        st.session_state.product_id = product[0]
                        self.delete_product(product)
                with cols[5]:
                    if st.button("Editar", key=f"edit_{product[0]}"):
                        self.prepare_edit(product)
            st.markdown("---")
