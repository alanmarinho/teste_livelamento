# Teste de Nivelamento Intuitive Care

- Candidato: Alan Marinho

## Pré-requisitos para execução

- Docker v27.3+ (para o banco)
- Python v3.12.3+
- Postman/Insomnia (para executar requests na API)
- Requisitos de `./requirements.txt` (para os scripts Python)

## Como executar

1. Clone o repositório: `git clone https://github.com/alanmarinho/teste_livelamento.git`
2. Instale as dependências Python: `pip install -r ./requirements.txt`
3. Execute: `python .\main.py`

- Nessa altura, a CLI deve aparecer no console com as opções de execução.
- Como um teste depende de dados de alguns dos anteriores, a ordem de execução deve ser a que aparece no CLI (pelo menos na primeira execução).

  ```
      Comandos:
      'exe 1' - executar TESTE DE WEB SCRAPING
      'exe 2' - executar TESTE DE TRANSFORMAÇÃO DE DADOS 
      'exe 3 db' - carregar os dados no banco
      'exe 3 q1' - query maires gasto no ultimo trimestre
      'exe 3 q1' - query maiores gastos no ultimo ano 
  ```
- OBS:
  - Testes que envolvem o banco são demorados, principalmente a opção de carregar dados, pois são 6M+ de ocorrências para carregar no banco.
  - Testes de API e front-end são executados manualmente fora do CLI.
  - A API usou o banco pois ele já estava implementado.
  - TODOS os comandos citados neste README devem ser executados a partir da raiz do projeto ou no CLI quando especificado.

## Teste 1 - WEB SCRAPING
  - Ao digitar no CLI o comando `exe 1`, o web scraping será executado, buscando na URL disponibilizada os dados exigidos, salvando-os na pasta `./web_scraping/pdfs` e também compactando-os e salvando em `./web_scraping/compacts` com o nome `anexos.zip`.

## Teste 2 - TRANSFORMAÇÃO DE DADOS
  - Ao digitar no CLI o comando `exe 2`, os processos exigidos serão executados sobre os dados anteriormente salvos em `./web_scraping/pdfs` (É IMPORTANTE QUE O COMANDO 1 SEJA EXECUTADO PRIMEIRO). O processamento do arquivo irá iniciar e, após a conclusão, os dados serão salvos em `./transformacao_dados/CSVs` no formato estruturado `.csv` e também compactados e salvos em `./transformacao_dados/compacts` com o nome `Teste_Alan_Marinho.zip`, conforme exigido.

## Teste 3 - BANCO DE DADOS
  ### Preparação
  1. É necessário executar uma instância de banco de dados MySQL em um container Docker. Para isso, execute (EM UM CONSOLE DIFERENTE DO DA CLI) `docker-compose -f .\banco_dados\docker-compose.yml up -d`. A mensagem `✔ Container db_alan_marinho Started` deve aparecer.
  2. Com o container rodando, execute no CLI o comando `exe 3 db` para criar as tabelas e povoar o banco com os dados dos arquivos `.csv` na pasta `./banco_dados/dados`. Serão criadas as tabelas `operadoras_de_plano_de_saude_ativas` e `demonstracoes_contabeis`, com o processo demorando cerca de 5 minutos. O processo é demorado devido à grande quantidade de dados carregados no banco, ultrapassando 6 milhões de itens nos arquivos exigidos do tópico "Tarefas de Preparação", onde os arquivos foram manualmente baixados (já que não foi exigido web scraping para eles). Após a execução da ação de povoamento de dados, as queries SQL podem ser executadas.

  ### Queries SQL
  1. APÓS o banco ser povoado, digite `exe 3 q1` para executar a primeira query exigida e `exe 3 q2` para executar a segunda query exigida. Após cada execução de query, os dados tabulados serão mostrados no console para cada query individualmente.

## Teste 4 - API

  ### API
  1. Para executar a API, digite em um console livre o comando `python .\api\main.py`. Uma API Flask deve ser iniciada e uma mensagem semelhante a ```* Running on http://127.0.0.1:5000``` será apresentada, e a API estará disponível na URL `http://127.0.0.1:5000`.
  2. Para usar a API, pode-se usar a coleção compatível com Postman/Insomnia disponibilizada em `./utils/colecao.json` e importá-la no programa de requests de sua preferência.
    ### Rotas
      - GET `/` - rota principal, retorna apenas uma mensagem indicando que a API está funcionando.
      - GET `/search_operadora?rs={text}` - Rota de busca por operadoras, busca no campo `Razao_Social` correspondências pelo texto fornecido `{text}` sob o parâmetro de URL `rs`.
      - Pode ser usado diretamente no navegador também, ex:
        - http://127.0.0.1:5000/
        - http://127.0.0.1:5000/search_operadora?rs=caixa

  ### Front Vue
  1. Em um console livre, execute os comandos em sequência `cd .\vue_front\` e `npm install` para se dirigir ao local do front-end e instalar as dependências.
  2. Execute o comando `npm run dev` para rodar o projeto, que pode ser acessado em `http://localhost:5173`. Lá, pode-se realizar uma busca pela `Razao_Social` das operadoras de plano de saúde de forma visual, utilizando o endpoint `/search_operadora?rs={text}` da API, e tabulando os dados.


  - Remover o container do banco após o uso é recomendado: `docker rm -f db_alan_marinho`


 <!-- -..- -....- -..- -->
