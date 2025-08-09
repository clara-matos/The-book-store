# 📖 The Book Store

## 📌 Sobre o Projeto

O **The Book Store** é uma aplicação web desenvolvida com o framework **Django**, que funciona como um sistema de gestão de livros.
A plataforma permite que os usuários descubram novos títulos, visualizem informações detalhadas sobre autores e gêneros, e registrem notas e progresso de leitura.

O projeto foca em:

* Uma arquitetura de dados sólida.
* Interface intuitiva e responsiva.
* Funcionalidades modernas, incluindo integração com IA.

---

## ✨ Funcionalidades Principais

* **📚 Gestão de Livros:** Visualize, adicione e gerencie uma biblioteca personalizada.
* **👩‍💼 Autores e Gêneros:** Classifique e organize os livros.
* **👤 Perfis de Usuário:** Cada usuário possui sua própria lista de livros e informações personalizadas.
* **📝 Notas de Leitura:** Registre e associe anotações a livros específicos.
* **💻 Interface Amigável:** Layout moderno e adaptado para dispositivos móveis e desktops.
* **🤖 Resumos com IA:** Integração com a **Google Gemini API** para gerar resumos cativantes.

---

## ⚙️ Modelagem de Dados

O modelo de dados foi criado com **django-extensions** e **pygraphviz**.

**Principais entidades:**

* **Autor:** Armazena dados dos autores.
* **Genero:** Classifica os livros por gênero literário.
* **PerfilUsuario:** Extende o modelo `User` do Django para dados personalizados.
* **Livro:** Modelo central, com relações para Autor, Genero e PerfilUsuario.
* **NotaDeLeitura:** Permite criar anotações associadas a livros.

---

## 🚀 Como Começar

### 📋 Pré-requisitos

* Python 3.8+
* pip (gerenciador de pacotes Python)
* Graphviz (necessário para gerar diagramas)

### 🔧 Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/The-book-store.git
cd The-book-store

# Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Instale as dependências
pip install -r requirements.txt

# Caso não exista requirements.txt:
pip install Django django-extensions pygraphviz Pillow

# Instale o Graphviz (Linux)
sudo apt-get update && sudo apt-get install -y graphviz libgraphviz-dev

# Migrações
python manage.py makemigrations
python manage.py migrate

# Crie um superusuário
python manage.py createsuperuser

# Execute o servidor
python manage.py runserver
```

Acesse: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Django
* **Banco de Dados:** SQLite (padrão)
* **Frontend:** HTML, CSS, Bootstrap 5
* **Ferramentas:** django-extensions, pygraphviz
* **Integração com IA:** Google Gemini API

---

## 👥 Equipe do Projeto

* **Pedro Guimel** – Co-desenvolvedor e arquiteto.
* **Erica Beatriz** – Desenvolvedora principal.
* **Clara Matos** – Contribuidora.

---

## 🛡️ Permissões de CRUD

| Modelo            | Criar        | Ler              | Atualizar        | Apagar           |
| ----------------- | ------------ | ---------------- | ---------------- | ---------------- |
| **Autor**         | Admin        | Todos            | Admin            | Admin            |
| **Genero**        | Admin        | Todos            | Admin            | Admin            |
| **PerfilUsuario** | Novo usuário | Logado           | Logado (próprio) | Admin            |
| **Livro**         | Logado       | Todos            | Logado (próprio) | Logado (próprio) |
| **NotaDeLeitura** | Logado       | Logado (próprio) | Logado (próprio) | Logado (próprio) |

> **Obs.:** "Logado (próprio)" significa que o usuário só pode editar/apagar os próprios registros.
> **Admin** refere-se a um superusuário no Django.

