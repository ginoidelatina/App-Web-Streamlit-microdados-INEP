# App-Web-Streamlit-microdados-INEP
# Aplicativo Web Streamlit que dispõe de estatísticas descritivas aplicadas à Educação Superior no Brasil.
Acesse -> <https://ginoidelatina-app-web-streamlit-micro-streamlit-app-inep-fd5zub.streamlit.app/>

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
  Instale o [Python 3.10](https://www.python.org/downloads)
  
  Instale o [PIP](https://pip.pypa.io/en/stable/installation)
  
  Utilize o editor de texto ou IDE de sua preferência. Para o desenvolvimento deste projeto, foi utilizado o [Visual Studio Code](https://code.visualstudio.com/download).


### 2. Configure o seu ambiente
  Independentemente da ferramenta de gerenciamento de pacotes que você está usando, é recomendado instalar os pacotes utilizados neste projeto em 
  um ambiente virtual. Isso garante que as dependências deste projeto não afetem nenhum outro projeto Python presente em seu sistema.
  Abaixo estão algumas ferramentas que você pode usar para gerenciamento de ambiente:
  - pipenv
  - poetry
  - venv
  - virtualenv
  - conda

  Neste projeto foi utilizado o anaconda, pois este oferece uma maneira fácil de  obter os principais pacotes de ciências de dados. Apesar da praticidade
  do anaconda, este apresenta algumas desvantagens relativas ao alto custo de memória e processamento.

  Na sequência (seção 2.1), instruirá como preparar o ambiente virtual utilizado por este projeto, se você não tem o interesse em utilizar o anaconda 
  como ferramenta de gerenciamento de pacotes, então pule para a seção 3.


### 2.1 Configurando o ambiente virtual com o Anaconda

[Clique aqui](https://docs.anaconda.com/anaconda/instal), para acessar o guia de instalação do anaconda, disponível para os principais sistemas operacionais.


Após instalar o anaconda em seu sistema, você precisará criar o seu ambiente de desenvolvimento. O Primeiro passo, é ativar o ambiente padrão do
anaconda em seu sistema. 


### 2.1.1 Ative o ambiente padrão do anaconda (chamado base)
  
#### Windows
Ative o ambiente padrão do anaconda no Windows

**Para versões do conda anteriores a 4.6:**

*Se o anaconda estiver instalado no PATH do sistema, digite:*

        C:\Anaconda3\Scripts\activate base 
	
*Se o anaconda estiver instalado em um diretório pessoal de usuário, digite:*

        C:\Users\seu_usuário\Anaconda3\Scripts conda activate base 
	
**Para o conda 4.6 e versões posteriores:**

*Se o anaconda estiver instalado no PATH do sistema, digite:* 

        C:\Anaconda3\Scripts\activate base
	
*Se o anaconda estiver instalado em um diretório pessoal de usuário, digite:*

        C:\Users\seu_usuário\Anaconda3\Scripts conda activate base

Dica: É possível verificar se o anaconda está instalado e em execução no seu sistema, por meio do comando:
conda --version

#### Linux ou macOS
Para ativar o anaconda no Linux ou macOS, localize o diretório onde o anaconda está instalado (por padrão, é chamado de anaconda3 ou
Anaconda3). Dentro do diretório do anaconda, navegue até a pasta ‘bin’, em seguida digite um dos comandos a seguir:

**Para o conda 4.6 e versões posteriores:**

        conda activate
	
**Para versões do conda anteriores a 4.6:**

        source activate 


### 2.1.2 Crie o seu ambiente virtual
Com o ambiente padrão do conda ativo, crie o seu próprio ambiente virtual. Veja a seguir como fazer isso:

	conda create --name envname python

Agora altere o envname pelo nome que você deseja dar ao seu ambiente virtual. 

Importante: Por padrão, o diretório de seu ambiente virtual estará localizado dentro de uma pasta chamada envs, que é um subdiretório padrão do
anaconda3. 


### 2.1.3 Ative o seu novo ambiente virtual:
  
**Para o conda 4.6 e versões posteriores:**
#### Windows
        
	conda activate envname
#### macOS ou Linux
        
	conda activate envname 

**Para versões do conda anteriores a 4.6, digite:**
#### Windows 
        
	activate envname
	
#### macOS e Linux
        
	source activate envname  



### 2.1.4 Instale as principais ferramentas - utilizadas neste projeto - em seu ambiente conda.
  
#### Github
Com seu ambiente virtual ativo, instale o git com o comando a seguir: 
      	
	conda install git

#### Python
Se o python estiver faltando em seu ambiente virtual, você pode usar o conda para instalá-lo. 
	
	conda install python

#### Pip
Se o pip estiver faltando em seu ambiente virtual, use o conda para instalá-lo.
      	
	conda install pip

Depois de ter instalado o pip, adicione os pacotes do requirements.txt deste projeto. Veja como fazer isso na seção 3.



#### Desativar o conda (opcional).

Se você quiser alternar projetos ou sair do seu ambiente virtual, basta executar:
      	
	conda deactivate ou deactivate
	
Se você quiser entrar novamente no ambiente virtual, basta seguir as mesmas instruções acima sobre como ativar um ambiente virtual. Não há necessidade
de reinstalar os programas e nem de recriar o ambiente virtual.


### 3. Instalando este repositório git em sua máquina local.
  
Importante: Independentemente da ferramenta de gerenciamento de pacotes que você está usando, não esqueça de ter em seu ambiente virtual o python e o o
pip. Também é recomendado instalar o git em seu ambiente.


### 3.1 Copie este repositório com o git em sua máquina local.
  
Com o seu ambiente virtual ativo, utilize o git para copiar este repositório em seu diretório local. Use o comando:
      	
	git clone https://github.com/ginoidelatina/projetointegradorII.git

### 3.2- Copie este repositório com o pip (é mais recomendável a opção acima).

Utilize o pip instalado em seu ambiente virtual ativo, para copiar o projeto deste repositório git em seu diretório local. Para isso, execute o
comando:
      	
	pip install -e git+https://github.com/ginoidelatina/projetointegradorII.git#egg=projetointegradorII


### 4. Instale os pacotes disponíveis no arquivo requirements.txt
Depois de ter copiado este repositório em sua máquina local, navegue até o diretório onde está localizado o arquivo requirements.txt. 
Em seguida, use o pip para instalar as dependências de requirements.txt

	pip install -r requirements.txt


### 5. Execute o código.

Para rodar o App Web, basta navegar até o diretório onde encontra-se o programa streamlit-app-inep. Em seguida, execute o seguinte script:

	streamlit run streamlit-app-inep.py 
	
Importante: Antes de executar o comando acima, certifique-se de ter o seu ambiente virtual ativo, assim como as dependências (requirements.txt)
instaladas em seu dispositivo.


