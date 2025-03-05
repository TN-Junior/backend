# Desafio Oncase

## Notion
https://www.notion.so/Desafio-Oncase-Full-Stack-1a904eaa22ab80428738f137f865cea1?pvs=4

## Visão Geral
Este projeto é uma aplicação Full Stack desenvolvida com React no front-end, Flask no back-end e MySQL para persistência de dados, com o banco de dados hospedado no AWS RDS. A aplicação apresenta uma interface onde o usuário pode inserir dados por meio de um formulário. Esses dados são armazenados em uma tabela MySQL e utilizados para atualizar dinamicamente um gráfico de pizza.

## Estrutura do Projeto
A estrutura do projeto está organizada de acordo com as responsabilidades de cada camada, facilitando a escalabilidade e manutenção da aplicação.

### Frontend
- **src/**
  - **assets/**: Contém os arquivos estáticos, como imagens e ícones.
  - **components/**: Contém os componentes reutilizáveis da aplicação, como formulários e tabelas.
  - **services/**: Contém a comunicação com a API Backend usando Axios.
  - **tests/**: Contém os testes automatizados para a aplicação frontend.
  - **types/**: Define os tipos TypeScript utilizados na aplicação.
  - **App.tsx**: Componente principal que organiza o fluxo da aplicação.
  - **index.css**: Arquivo de estilos globais.
  - **main.tsx**: Ponto de entrada da aplicação React.
  - **vite-env.d.ts**: Definições de ambiente para o Vite.

### Backend
- **backend/**
  - **app/**
    - **__init__.py**: Inicialização do módulo da aplicação.
    - **config.py**: Contém a configuração da conexão com o banco de dados.
    - **database.py**: Define a lógica de conexão e manipulação do banco de dados.
    - **models.py**: Define os modelos de dados utilizados na aplicação.
    - **routes.py**: Define as rotas e endpoints da API.
  - **tests/**
    - **test_models.py**: Código para testes do modelo.
    - **test_routes.py**: Código para testes das rotas.
  - **requirements.txt**: Arquivo que lista as dependências do backend.
  - **run.py**: Script de inicialização da aplicação backend.

## Funcionalidades Implementadas

### Frontend:
- **Formulário de Inserção de Dados**: Permite o preenchimento de dados, com validação de campos obrigatórios.
- **Tabela de Exibição**: Exibe a lista de participantes, com funcionalidades de edição e exclusão.
- **Gráfico de Pizza**: Representa a distribuição de dados de participantes, facilitando a visualização da participação de cada um.
- **Loader no Botão de Envio**: Implementação de um loader visual para melhorar a experiência do usuário enquanto os dados são processados.

### Backend:
- **API RESTful**: A aplicação fornece uma API RESTful para interagir com os dados, incluindo endpoints para inserção, listagem, edição e exclusão.
- **Validação de Erros**: A API realiza a validação de erros de entrada de dados e retorna mensagens apropriadas com código HTTP adequado.
- **Banco de Dados**: Utiliza um banco de dados para persistir as informações de participantes. Foi utilizado um banco de dados MySQL para armazenar as entidades.
- **Tratamento de Exceções**: Exceções específicas são tratadas e retornadas com status HTTP adequado, utilizando uma abordagem de gerenciamento centralizado de erros.


## Boas Práticas de Desenvolvimento

Organização do Código: O código é modularizado, com componentes reutilizáveis e bem organizados. As funções são separadas por responsabilidades, e os componentes React são compostos de forma clara.


Tratamento de Exceções: O tratamento de exceções é feito no backend com blocos try-except para capturar erros durante as operações de banco de dados e nas rotas, garantindo respostas apropriadas em caso de falhas.


Controle de Versão: O código está versionado com Git. Cada commit reflete modificações significativas, como a adição de funcionalidades ou ajustes em componentes e estilos, com mensagens de commit claras.


Testes: Foram implementados testes unitários e de integração utilizando o Jest e o Testing Library no frontend e pytest no backend. Esses testes garantem a validade da lógica de formulários, operações CRUD e validações de dados.


Performance: A performance é otimizada com uso de hooks do React como useCallback para evitar renders desnecessários e useEffect para carregar dados de maneira eficiente. No backend, o uso do SQLAlchemy para consultas e manipulação de dados é eficiente.


Segurança: O backend utiliza CORS para controlar as origens permitidas, protegendo as rotas da aplicação. Além disso, a configuração do banco de dados garante segurança nas credenciais e na comunicação via ambiente.


 
## Interface
 
  ![image](https://github.com/user-attachments/assets/3f9ce7d5-9116-4e3d-8641-d128304a1415)




