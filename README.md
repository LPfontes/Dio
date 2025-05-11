### Resumo da Aplicação

Esta aplicação é um **sistema de cadastro e gerenciamento de produtos** desenvolvido com **Streamlit** e integrado ao **Azure Blob Storage** e **SQL Server**. Ela permite que os usuários realizem as seguintes operações:

1. **Cadastrar Produtos**:
   - Os usuários podem preencher um formulário com o nome, preço, descrição e imagem do produto.
   - A imagem é processada e enviada para o Azure Blob Storage, e a URL gerada é salva no banco de dados.

2. **Editar Produtos**:
   - Os produtos cadastrados podem ser editados diretamente na interface.
   - É possível alterar o nome, preço, descrição e imagem do produto.

3. **Listar Produtos**:
   - Os produtos cadastrados são exibidos em uma lista paginada.
   - Cada produto exibe sua imagem, nome, descrição e preço.

4. **Deletar Produtos**:
   - Os usuários podem excluir produtos, removendo-os do banco de dados e deletando a imagem associada do Azure Blob Storage.

---

### Principais Componentes
Escolhi separar o projeto em 3 partes.
1. **`ProductApp`**:
   - Classe principal que gerencia a interface do usuário e as interações.
   - Contém métodos para renderizar formulários, processar imagens e exibir a lista de produtos.

2. **`ControlDB`**:
   - Classe responsável pela integração com o banco de dados SQL Server e o Azure Blob Storage.
   - Gerencia operações como salvar, listar, atualizar e deletar produtos.

3. **main.py**:
   - Arquivo principal que inicializa a aplicação.
   - Cria uma instância de `ProductApp` e chama os métodos para configurar o formulário e exibir a lista de produtos.

---

### Fluxo da Aplicação

1. **Inicialização**:
   - O arquivo main.py cria uma instância de `ProductApp` e chama os métodos `setup_form` e `render_product_list`.

2. **Cadastro de Produtos**:
   - O formulário é exibido para o usuário preencher os dados do produto.
   - Após o envio, os dados são validados e salvos no banco de dados, e a imagem é redimensionada para 300x300 pixels, convertida para webp para otimizar recursos e enviada para o Azure Blob Storage.

3. **Edição de Produtos**:
   - O usuário pode selecionar um produto para editar.
   - As alterações são salvas no banco de dados, e uma nova imagem pode ser enviada para substituir a anterior.

4. **Exclusão de Produtos**:
   - O usuário pode excluir um produto, removendo-o do banco de dados e deletando a imagem associada do Azure Blob Storage.

---

### Tecnologias Utilizadas

- **Streamlit**: Para criar a interface do usuário.
- **Azure Blob Storage**: Para armazenar as imagens dos produtos.
- **SQL Server**: Para armazenar os dados dos produtos.
- **Python**: Linguagem principal para o desenvolvimento da aplicação.
- **Pillow**: Para manipulação de imagens.
---

### Objetivo

O objetivo da aplicação é fornecer uma interface simples e eficiente para gerenciar produtos, com suporte para upload de imagens e integração com serviços em nuvem.
