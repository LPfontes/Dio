from ProductApp import ProductApp
#Esta aplicação é um sistema de cadastro e gerenciamento de produtos desenvolvido com Streamlit 
# e integrado ao Azure Blob Storage e SQL Server. 

# Inicializa o aplicativo
if __name__ == "__main__":
    app = ProductApp()
    app.setup_form()
    app.render_product_list()
#                     
