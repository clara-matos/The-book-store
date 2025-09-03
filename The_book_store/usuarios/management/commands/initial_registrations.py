# usuario/management/commands/initial_setup.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, transaction, connection
from datetime import date, timedelta
import sys
import random

# Importa todos os modelos do projeto The Book Store
from django.contrib.auth.models import User
from livros.models import Livro, Autor, Genero
from usuarios.models import PerfilUsuario
from notas.models import NotaDeLeitura

class Command(BaseCommand):
    help = 'Executa o setup inicial do projeto The Book Store, criando grupos, usuários de teste e dados de exemplo.'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.autores = {}
        self.generos = {}
        self.users = {}
        self.livros = {}

    def handle(self, *args, **options):
        # Verificar se as migrações foram aplicadas
        if not self._check_migrations_applied():
            self.stdout.write(self.style.ERROR(
                "Erro: Migrações do Django não foram aplicadas. "
                "Execute 'python manage.py migrate' primeiro."
            ))
            sys.exit(1)
            
        self.stdout.write(self.style.SUCCESS("Iniciando o setup inicial do The Book Store..."))

        try:
            with transaction.atomic():
                self._setup_groups_and_permissions()
                self._setup_admin_user()
                self._setup_autores()
                self._setup_generos()
                self._setup_dev_users()
                self._setup_livros()
                self._setup_notas_de_leitura()
            
            self.stdout.write(self.style.SUCCESS("\nSetup inicial do The Book Store concluído com sucesso!"))
            self._show_login_credentials()
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro durante o setup: {str(e)}"))
            raise

    def _check_migrations_applied(self):
        """Verifica se as migrações básicas do Django foram aplicadas"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_group'")
                return cursor.fetchone() is not None
        except:
            return False

    def _setup_groups_and_permissions(self):
        """Configura grupos e permissões para The Book Store"""
        self.stdout.write(self.style.SUCCESS("\n--- Criando Grupos e Permissões ---"))
        
        groups_permissions_map = {
            'Leitores': [
                ('view_livro', Livro),
                ('view_autor', Autor),
                ('view_genero', Genero),
                ('add_notadeleitura', NotaDeLeitura),
                ('view_notadeleitura', NotaDeLeitura),
                ('change_notadeleitura', NotaDeLeitura),
            ],
            'Editores': [
                ('view_livro', Livro),
                ('add_livro', Livro),
                ('change_livro', Livro),
                ('delete_livro', Livro),
                ('view_autor', Autor),
                ('add_autor', Autor),
                ('change_autor', Autor),
                ('delete_autor', Autor),
                ('view_genero', Genero),
                ('add_genero', Genero),
                ('change_genero', Genero),
                ('delete_genero', Genero),
                ('view_notadeleitura', NotaDeLeitura),
                ('delete_notadeleitura', NotaDeLeitura),
            ],
            'Administradores': [
                ('view_livro', Livro),
                ('add_livro', Livro),
                ('change_livro', Livro),
                ('delete_livro', Livro),
                ('view_autor', Autor),
                ('add_autor', Autor),
                ('change_autor', Autor),
                ('delete_autor', Autor),
                ('view_genero', Genero),
                ('add_genero', Genero),
                ('change_genero', Genero),
                ('delete_genero', Genero),
                ('view_notadeleitura', NotaDeLeitura),
                ('add_notadeleitura', NotaDeLeitura),
                ('change_notadeleitura', NotaDeLeitura),
                ('delete_notadeleitura', NotaDeLeitura),
                ('view_perfilusuario', PerfilUsuario),
                ('change_perfilusuario', PerfilUsuario),
            ],
        }

        def get_permission(codename, model):
            try:
                content_type = ContentType.objects.get_for_model(model)
                return Permission.objects.get(codename=codename, content_type=content_type)
            except (ContentType.DoesNotExist, Permission.DoesNotExist):
                return None

        for group_name, permissions_list in groups_permissions_map.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Grupo '{group.name}' criado com sucesso."))
            else:
                self.stdout.write(self.style.WARNING(f"Grupo '{group.name}' já existe."))
            
            for codename, model in permissions_list:
                perm = get_permission(codename, model)
                if perm:
                    try:
                        group.permissions.add(perm)
                    except IntegrityError:
                        pass
                else:
                    self.stdout.write(self.style.WARNING(
                        f"Permissão '{codename}' para {model.__name__} não encontrada"
                    ))
        
        self.stdout.write(self.style.SUCCESS("Processo de grupos e permissões concluído."))

    def _setup_admin_user(self):
        """Configura usuário admin"""
        self.stdout.write(self.style.SUCCESS("\n--- Criando Admin de Desenvolvimento ---"))
        
        username = 'admin'
        email = 'admin@thebookstore.com'
        password = 'admin123'  # Senha mais segura

        if not User.objects.filter(username=username).exists():
            admin_user = User.objects.create_superuser(username, email, password)
            # Criar perfil para o admin
            PerfilUsuario.objects.create(user=admin_user, biografia="Administrador do sistema The Book Store")
            self.stdout.write(self.style.SUCCESS(f"Admin '{username}' criado com sucesso."))
        else:
            self.stdout.write(self.style.WARNING(f"Admin '{username}' já existe."))

    def _setup_autores(self):
        """Configura autores iniciais"""
        self.stdout.write(self.style.SUCCESS("\n--- Criando Autores ---"))
        
        autores_data = [
            {'nome': 'George Orwell', 'pais': 'Reino Unido', 'biografia': 'Escritor e jornalista inglês, conhecido por suas distopias políticas.'},
            {'nome': 'J.K. Rowling', 'pais': 'Reino Unido', 'biografia': 'Escritora britânica, autora da série Harry Potter.'},
            {'nome': 'J.R.R. Tolkien', 'pais': 'Reino Unido', 'biografia': 'Escritor, professor e filólogo britânico, autor de O Senhor dos Anéis.'},
            {'nome': 'Jane Austen', 'pais': 'Reino Unido', 'biografia': 'Romancista britânica considerada uma das maiores escritoras da literatura inglesa.'},
            {'nome': 'Machado de Assis', 'pais': 'Brasil', 'biografia': 'Escritor brasileiro, widely regarded as the greatest writer of Brazilian literature.'},
            {'nome': 'Stephen King', 'pais': 'EUA', 'biografia': 'Escritor norte-americano de terror, ficção sobrenatural, suspense e ficção científica.'},
            {'nome': 'Agatha Christie', 'pais': 'Reino Unido', 'biografia': 'Escritora britânica que se notabilizou no gênero policial.'},
            {'nome': 'Clarice Lispector', 'pais': 'Brasil', 'biografia': 'Escritora e jornalista brasileira, considerada uma das mais importantes escritoras do século XX.'},
            {'nome': 'Isaac Asimov', 'pais': 'Rússia/EUA', 'biografia': 'Escritor e bioquímico americano, autor de obras de ficção científica e divulgação científica.'},
            {'nome': 'Gabriel García Márquez', 'pais': 'Colômbia', 'biografia': 'Escritor, jornalista e ativista político colombiano, laureado com o Nobel de Literatura.'},
        ]
        
        for autor_data in autores_data:
            autor, created = Autor.objects.get_or_create(
                nome=autor_data['nome'],
                defaults={
                    'pais': autor_data['pais'],
                    'biografia': autor_data['biografia']
                }
            )
            self.autores[autor.nome] = autor
            if created:
                self.stdout.write(self.style.SUCCESS(f"Autor '{autor.nome}' criado com sucesso."))
            else:
                self.stdout.write(self.style.WARNING(f"Autor '{autor.nome}' já existe."))

    def _setup_generos(self):
        """Configura gêneros literários"""
        self.stdout.write(self.style.SUCCESS("\n--- Criando Gêneros Literários ---"))
        
        generos_data = [
            {'nome': 'Ficção Científica', 'descricao': 'Narrativas que exploram conceitos científicos e tecnológicos.'},
            {'nome': 'Fantasia', 'descricao': 'Obras com elementos mágicos, mitológicos e sobrenaturais.'},
            {'nome': 'Romance', 'descricao': 'Narrativas longas que exploram relacionamentos e desenvolvimento de personagens.'},
            {'nome': 'Terror', 'descricao': 'Obras que provocam medo e suspense no leitor.'},
            {'nome': 'Mistério', 'descricao': 'Narrativas centradas na solução de um crime ou enigma.'},
            {'nome': 'Distopia', 'descricao': 'Obras que retratam sociedades futuras indesejáveis.'},
            {'nome': 'Literatura Brasileira', 'descricao': 'Obras de autores brasileiros.'},
            {'nome': 'Clássico', 'descricao': 'Obras literárias consideradas canônicas e de valor duradouro.'},
            {'nome': 'Realismo Mágico', 'descricao': 'Gênero literário que incorpora elementos mágicos em ambientes realistas.'},
            {'nome': 'Biografia', 'descricao': 'Narrativas sobre a vida de pessoas reais.'},
        ]
        
        for genero_data in generos_data:
            genero, created = Genero.objects.get_or_create(
                nome=genero_data['nome'],
                defaults={'descricao': genero_data['descricao']}
            )
            self.generos[genero.nome] = genero
            if created:
                self.stdout.write(self.style.SUCCESS(f"Gênero '{genero.nome}' criado com sucesso."))
            else:
                self.stdout.write(self.style.WARNING(f"Gênero '{genero.nome}' já existe."))

    def _setup_dev_users(self):
        """Configura usuários de desenvolvimento"""
        self.stdout.write(self.style.SUCCESS("\n--- Criando Utilizadores de Desenvolvimento ---"))
        
        dev_users_data = [
            {
                'username': 'leitor1', 'email': 'leitor1@thebookstore.com', 'password': 'leitor123',
                'group': 'Leitores', 'is_staff': False,
                'perfil_data': {
                    'biografia': 'Amante de livros de fantasia e ficção científica.',
                    'data_nascimento': date(1995, 5, 15),
                }
            },
            {
                'username': 'leitor2', 'email': 'leitor2@thebookstore.com', 'password': 'leitor123',
                'group': 'Leitores', 'is_staff': False,
                'perfil_data': {
                    'biografia': 'Interessado em clássicos da literatura e romances.',
                    'data_nascimento': date(1990, 8, 22),
                }
            },
            {
                'username': 'editor1', 'email': 'editor1@thebookstore.com', 'password': 'editor123',
                'group': 'Editores', 'is_staff': True,
                'perfil_data': {
                    'biografia': 'Editor experiente com paixão por descobrir novos talentos.',
                    'data_nascimento': date(1985, 3, 10),
                }
            },
            {
                'username': 'admin2', 'email': 'admin2@thebookstore.com', 'password': 'admin456',
                'group': 'Administradores', 'is_staff': True,
                'perfil_data': {
                    'biografia': 'Administrador do sistema The Book Store.',
                    'data_nascimento': date(1980, 11, 5),
                }
            },
        ]

        self.users = {}
        for user_data in dev_users_data:
            user = self._create_dev_user(user_data)
            self.users[user.username] = user

    def _create_dev_user(self, user_data):
        """Cria um usuário de desenvolvimento"""
        username = user_data['username']
        
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': user_data['email'],
                'is_staff': user_data.get('is_staff', False),
            }
        )
        
        if created:
            user.set_password(user_data['password'])
            user.save()
            # Criar perfil do usuário
            PerfilUsuario.objects.create(user=user, **user_data['perfil_data'])
            self.stdout.write(self.style.SUCCESS(f"Utilizador '{username}' criado com sucesso."))
        else:
            self.stdout.write(self.style.WARNING(f"Utilizador '{username}' já existe."))
            # Atualizar senha se o usuário já existe
            user.set_password(user_data['password'])
            user.save()
        
        try:
            group = Group.objects.get(name=user_data['group'])
            user.groups.add(group)
            self.stdout.write(self.style.SUCCESS(f"  - Adicionado ao grupo: {user_data['group']}"))
        except Group.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"  - Grupo '{user_data['group']}' não encontrado."))
        
        return user
    
    def _setup_livros(self):
        """Configura livros iniciais"""
        self.stdout.write(self.style.SUCCESS("\n--- Criando Livros ---"))
        
        livros_data = [
            {
                'titulo': '1984', 
                'autor': self.autores['George Orwell'],
                'genero': self.generos['Distopia'],
                'lido': True,
            },
            {
                'titulo': 'Harry Potter e a Pedra Filosofal', 
                'autor': self.autores['J.K. Rowling'],
                'genero': self.generos['Fantasia'],
                'lido': False,
            },
            {
                'titulo': 'O Senhor dos Anéis: A Sociedade do Anel', 
                'autor': self.autores['J.R.R. Tolkien'],
                'genero': self.generos['Fantasia'],
                'lido': True,
            },
            {
                'titulo': 'Orgulho e Preconceito', 
                'autor': self.autores['Jane Austen'],
                'genero': self.generos['Romance'],
                'lido': False,
            },
            {
                'titulo': 'Dom Casmurro', 
                'autor': self.autores['Machado de Assis'],
                'genero': self.generos['Literatura Brasileira'],
                'lido': True,
            },
            {
                'titulo': 'O Iluminado', 
                'autor': self.autores['Stephen King'],
                'genero': self.generos['Terror'],
                'lido': False,
            },
            {
                'titulo': 'Assassinato no Expresso Oriente', 
                'autor': self.autores['Agatha Christie'],
                'genero': self.generos['Mistério'],
                'lido': True,
            },
            {
                'titulo': 'A Hora da Estrela', 
                'autor': self.autores['Clarice Lispector'],
                'genero': self.generos['Literatura Brasileira'],
                'lido': False,
            },
            {
                'titulo': 'Fundação', 
                'autor': self.autores['Isaac Asimov'],
                'genero': self.generos['Ficção Científica'],
                'lido': True,
            },
            {
                'titulo': 'Cem Anos de Solidão', 
                'autor': self.autores['Gabriel García Márquez'],
                'genero': self.generos['Realismo Mágico'],
                'lido': False,
            },
        ]
        
        self.livros = {}
        for livro_data in livros_data:
            livro, created = Livro.objects.get_or_create(
                titulo=livro_data['titulo'],
                autor=livro_data['autor'],
                defaults={
                    'genero': livro_data['genero'],
                    'lido': livro_data['lido'],
                    'usuario': self.users['leitor1'].perfil if livro_data['lido'] else None
                }
            )
            self.livros[livro.titulo] = livro

            if created:
                self.stdout.write(self.style.SUCCESS(f"Livro '{livro.titulo}' criado com sucesso."))
            else:
                self.stdout.write(self.style.WARNING(f"Livro '{livro.titulo}' já existe."))
    
    def _setup_notas_de_leitura(self):
        """Configura notas de leitura iniciais"""
        self.stdout.write(self.style.SUCCESS("\n--- Criando Notas de Leitura ---"))
        
        notas_data = [
            {
                'livro': self.livros['1984'],
                'usuario': self.users['leitor1'].perfil,
                'comentario': 'Uma distopia assustadoramente relevante até hoje. Leitura obrigatória!',
            },
            {
                'livro': self.livros['O Senhor dos Anéis: A Sociedade do Anel'],
                'usuario': self.users['leitor1'].perfil,
                'comentario': 'Fantasia épica no seu melhor. Tolkien é um mestre da worldbuilding.',
            },
            {
                'livro': self.livros['Dom Casmurro'],
                'usuario': self.users['leitor1'].perfil,
                'comentario': 'Machado de Assis em sua genialidade. A ambiguidade de Bentinho é fascinante.',
            },
            {
                'livro': self.livros['Fundação'],
                'usuario': self.users['leitor1'].perfil,
                'comentario': 'Uma das melhores séries de ficção científica já escritas. Asimov era visionário.',
            },
        ]
        
        for nota_data in notas_data:
            nota, created = NotaDeLeitura.objects.get_or_create(
                livro=nota_data['livro'],
                usuario=nota_data['usuario'],
                defaults={'comentario': nota_data['comentario']}
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f"Nota criada: {nota.usuario.user.username} para '{nota.livro.titulo}'"
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f"Nota já existe: {nota.usuario.user.username} para '{nota.livro.titulo}'"
                ))
    
    def _show_login_credentials(self):
        """Mostra as credenciais de login após o setup"""
        self.stdout.write(self.style.SUCCESS("\n--- Credenciais de Login ---"))
        self.stdout.write(self.style.WARNING("Admin: usuario=admin, senha=admin123"))
        self.stdout.write(self.style.WARNING("Leitor 1: usuario=leitor1, senha=leitor123"))
        self.stdout.write(self.style.WARNING("Leitor 2: usuario=leitor2, senha=leitor123"))
        self.stdout.write(self.style.WARNING("Editor: usuario=editor1, senha=editor123"))
        self.stdout.write(self.style.WARNING("Admin 2: usuario=admin2, senha=admin456"))