from ProductApp import ProductApp
# Inicializa o aplicativo
if __name__ == "__main__":
    app = ProductApp()
    app.setup_form()
    app.render_product_list()