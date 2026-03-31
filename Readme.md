🖥️ ONG Asben - Sistema de Gestão Desktop (App)
Este repositório contém o aplicativo desktop da ONG Asben, desenvolvido para ser a ferramenta de trabalho exclusiva dos funcionários da instituição em Carapicuíba, SP. O foco deste software é a gestão administrativa, validação de cadastros e controle do ciclo de vida dos beneficiários.

🚀 Funcionalidades Administrativas
Gestão de Beneficiários (CRUD): Visualização, edição e exclusão de registros em tempo real.

Filtro Inteligente: Busca dinâmica por Nome ou CPF, eliminando a lentidão das antigas planilhas de Excel.

Visualização de Perfil: Exibição de cards com fotos dos assistidos, facilitando o reconhecimento facial no atendimento.

Controle de Status: Ferramenta para inativar ou excluir registros em casos de mudança de cidade ou falecimento, mantendo o banco de dados sempre atualizado.

Otimização de Imagem: Processamento automático (redimensionamento e compressão) antes do upload para o Supabase Storage.

🛠️ Tecnologias Utilizadas
Python 3: Linguagem base do projeto.

CustomTkinter: Biblioteca para criação de uma interface moderna e intuitiva.

Pillow (PIL): Manipulação e otimização de imagens de perfil.

Requests & IO: Comunicação com a nuvem para download e exibição de miniaturas.

Supabase Python SDK: Integração direta com o banco de dados PostgreSQL e Bucket de imagens.

📂 Estrutura do Projeto
Plaintext
├── main.py             # Arquivo principal (Interface CustomTkinter)
├── database.py         # Lógica de comunicação com o Supabase
├── .env                # Configurações de URL e KEY do projeto
└── requirements.txt    # Lista de dependências do Python
⚙️ Como Executar o App
Clone o repositório:

Bash
git clone https://github.com/Sidney00131/ong-asben-app.git
Instale as dependências:

Bash
pip install customtkinter supabase python-dotenv Pillow requests
Configuração de Ambiente:
Certifique-se de que o arquivo .env contenha as mesmas credenciais do Supabase utilizadas na versão Web.

Inicie a aplicação:

Bash
python main.py
📈 Impacto Operacional
O aplicativo resolve o problema do "dado morto". Enquanto o site coleta a informação, o App permite que o funcionário tome decisões, limpe o banco de dados e localize qualquer pessoa em menos de 1 segundo. Isso humaniza o atendimento e profissionaliza a assistência social em Carapicuíba.

Desenvolvido por Alan Vieira.

Estudante de Análise e Desenvolvimento de Sistemas - UNIFECAF.