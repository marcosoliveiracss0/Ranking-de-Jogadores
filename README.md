Sistema de Ranking de Jogadores (GUI)


Este é um sistema de ranking de jogadores desenvolvido em Python com uma interface gráfica (GUI) construída com a biblioteca Tkinter. O programa lê os dados dos jogadores a partir de um arquivo CSV, exibe um ranking ordenado pela pontuação e registra quaisquer erros de formatação em um arquivo de log para fácil depuração.

Screenshot da Aplicação
(Dica: Rode o programa, carregue um arquivo, tire um print da tela principal, salve essa imagem no seu repositório e atualize o caminho abaixo!)

✨ Funcionalidades
Interface Gráfica Amigável: Não precisa de terminal! Toda a interação é feita através de botões e janelas.

Seleção de Arquivo Interativa: Clique em um botão para abrir o gerenciador de arquivos do seu sistema e selecionar o arquivo .csv com os dados.

Ranking Visual e Ordenado: Exibe os jogadores em uma tabela clara, ordenados da maior para a menor pontuação.


Destaque para o Top 3: Os três primeiros colocados são destacados com cores especiais para fácil identificação.


Validação de Dados e Log de Erros: Linhas mal formatadas no CSV são ignoradas e registradas no arquivo erros.log, que pode ser visualizado diretamente pela interface.

Tratamento Inteligente de Linhas: Linhas em branco no arquivo de dados são automaticamente ignoradas, evitando falsos erros.

🚀 Como Executar
Requisitos
Python 3.x

Nenhuma biblioteca externa é necessária, pois o programa utiliza apenas módulos padrão do Python (Tkinter, CSV, OS).

Passo a Passo
Clone o Repositório

Bash

git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
cd SEU-REPOSITORIO
Prepare seu Arquivo de Dados
Certifique-se de ter um arquivo .csv pronto para ser lido. Veja a seção "Formato do Arquivo CSV" abaixo para mais detalhes.

Execute o Programa
Abra seu terminal na pasta do projeto e execute o seguinte comando:

Bash

python ranking_gui.py
Use a Aplicação

Clique em 📂 Selecionar Arquivo CSV para carregar seus dados.

Visualize o ranking na tela principal.

Clique em 📄 Ver Log de Erros para inspecionar linhas que não puderam ser carregadas.

📄 Formato do Arquivo CSV
Para que o programa funcione corretamente, o arquivo de entrada (.csv) deve seguir um formato específico.

A primeira linha do arquivo 

deve ser o cabeçalho: nome,nivel,pontuacao.

Cada linha subsequente deve conter os dados de um jogador, seguindo a ordem das colunas:


Nome (string) 


Nível (número inteiro) 


Pontuação (número, pode ter casas decimais) 

Exemplo de jogadores.csv válido:
Snippet de código

nome,nivel,pontuacao
Alice,10,1500.50
Bruno,8,1250.75
Carlos,12,1800.00
