# App-Web-Streamlit-microdados-INEP
# Aplicativo Web Streamlit que dispõe de estatísticas descritivas aplicadas à Educação Superior no Brasil.
Acesse a página -> <https://ginoidelatina-app-web-streamlit-micro-streamlit-app-inep-fd5zub.streamlit.app/>

Este projeto utiliza a linguagem python com as bibliotecas pandas, dask e matplotlib, assim como o framework web streamlit. 
Até o momento da última atualização deste projeto, a fonte de dados  - microdados do censo da educação superior 2021 - encontra-se acessível no 
portal do INEP: 

<https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-da-educacao-superior>

Também é possível acessar os dados no Portal Brasileiro de Dados Abertos:

<https://dados.gov.br/dados/conjuntos-dados/inep-microdados-do-censo-da-educacao-superior>

## Informações

Por meio dos Microdados, é possível obter um amplo panorama da educação brasileira. Esse é indubitavelmente um rico acervo sobre a educação superior 
do nosso país e uma fonte segura e eficaz de obtenção de dados, acessíveis aos pesquisadores, estudantes, gestores e sociedade em geral.

Originalmente, o arquivo ZIP Microdados do Censo da Educação Superior 2021, contém um diretório chamado dados. Dentro deste diretório existem dois
arquivos estruturados no formato CSV (Comma-Separated Values), delimitados por ponto-e-vírgula (;), nomeados como MICRODADOS_CADASTRO_IES_2021.CSV
MICRODADOS_CADASTRO_CURSOS_2021.CSV. Também é possível acessar o dicionário de dados dentro do diretório Anexos.

Todavia, para obter uma maior performance, o App Web deste projeto não utiliza os arquivos originais, mas sim um arquivo transformado que mantém apenas
os atributos de interesse, dos quais os registros permanecem intactos. Esta redução de dados melhora a eficiência da importação de dados e, também, reduz
os requisitos de armazenamento.

Outra transformação, foi a união dos arquivos MICRODADOS_CADASTRO_IES_2021.CSV e o MICRODADOS_CADASTRO_CURSOS_2020.CSV, em um único arquivo PARQUET,
chamado microdados2021-INEP.parquet, que encontra-se disponível neste repositório git, na pasta dados. Importante ressaltar, que a escolha do formato
PARQUET não é por acaso, os arquivos Parquet (orientados a coluna) ocupam muito menos espaço em disco do que arquivos CSVs (orientados a registros) 
e são mais rápidos de verificar. de serem verificados.


## Instruções

### 1. Pré-requesitos
  Instale o [Python 3.11.0](https://www.python.org/downloads)
  
  Instale o [PIP 23.3.1](https://pip.pypa.io/en/stable/installation)
  
  Utilize o editor de texto ou IDE de sua preferência. Para o desenvolvimento deste projeto, foi utilizado o [Visual Studio Code](https://code.visualstudio.com/download).



### 2. Configure o seu ambiente
  Independentemente da ferramenta de gerenciamento de pacotes que você está usando, é recomendado instalar os pacotes utilizados neste projeto em um ambiente virtual. Isso garante que as dependências deste projeto não afetem nenhum outro projeto Python presente em seu sistema.
  Abaixo estão algumas ferramentas que você pode usar para gerenciamento de ambiente:
  - pipenv
  - poetry
  - venv
  - virtualenv
  - conda

Neste projeto, escolhemos utilizar o **Anaconda** para configurar o ambiente virtual devido à sua praticidade, sendo uma escolha frequente para facilitar a aquisição dos principais pacotes de ciência de dados. Apesar da conveniência, é essencial observar que o Anaconda apresenta algumas desvantagens, como o elevado consumo de memória e processamento.

  Na sequência (seção 2.1), instruirá como preparar o ambiente virtual utilizado por este projeto, se você não tem o interesse em utilizar o anaconda como ferramenta de gerenciamento de pacotes, então pule para a seção 3.


### 2.1 Configurando o ambiente virtual com o Anaconda
#### Instale a versão 4.13.0 do Anaconda.
[Clique aqui](https://docs.anaconda.com/anaconda/instal), para acessar o guia de instalação do anaconda, disponível para os principais sistemas operacionais.

Após a instalação do Anaconda em seu sistema, é necessário configurar o ambiente de desenvolvimento. O primeiro passo consiste em ativar o ambiente padrão do Anaconda em seu sistema.


### 2.1.1 Ative o ambiente padrão do anaconda (chamado base)
  
#### Linux ou macOS
Para ativar o anaconda no Linux ou macOS, localize o diretório onde o anaconda está instalado (por padrão, é chamado de anaconda3 ou
Anaconda3). Dentro do diretório do anaconda, navegue até a pasta ‘bin’, em seguida digite um dos comandos a seguir:

	source activate base


### 2.1.2 Crie o seu ambiente virtual
Com o ambiente padrão do conda ativo, crie o seu próprio ambiente virtual. Veja a seguir como fazer isso:

	conda create -n envname python=3.11.0

Agora altere o envname pelo nome que você deseja dar ao seu ambiente virtual. 


### 2.1.3 Localize o diretório criado para o seu ambiente virtual.
Por padrão, o diretório de seu ambiente virtual estará localizado dentro de uma pasta chamada envs, que é um subdiretório padrão do anaconda3.
	
 	~/anaconda3/envs/


### 2.1.4 Ative o seu novo ambiente virtual:
No diretório do seu ambiente virtual, execute o seguinte comando:

#### macOS e Linux
        
	```source activate envname  


### 2.1.5 Instale o git em seu ambiente virtual.
Com seu ambiente virtual ativo, instale o git com o comando a seguir: 
      	
	conda install git



### 3. Instalando este repositório git em sua máquina local.
  
***Nota:** Certifique-se de que seu ambiente virtual inclua o Python, o Pip e o Git, independentemente da ferramenta de gerenciamento de pacotes que você estiver utilizando.*
  
Com o ambiente virtual configurado, utilize o Git para clonar este repositório no diretório correspondente ao seu ambiente virtual. Use o comando:
      	
	git clone https://github.com/ginoidelatina/App-Web-Streamlit-microdados-INEP.git



### 4. Instale os pacotes disponíveis no arquivo requirements.txt
Após clonar este repositório Git em sua máquina local, vá para a subpasta do projeto "App-Web-Streamlit-microdados-INEP.git" onde o arquivo requirements.txt está localizado.

Em seguida, utilize o pip para instalar as dependências listadas no arquivo `requirements.txt`.

	pip install -r requirements.txt



### 5. Execute o código.
Para rodar o App Web, basta navegar até o diretório onde encontra-se o programa streamlit-app-inep. Em seguida, execute o seguinte script:

	streamlit run streamlit-app-inep.py 
	
Importante: Antes de executar o comando acima, certifique-se de ter o seu ambiente virtual ativo, assim como as dependências (requirements.txt)
instaladas em seu dispositivo.


