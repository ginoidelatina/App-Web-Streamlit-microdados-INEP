import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg
_lock = RendererAgg.lock
import matplotlib.style as style
from io import BytesIO
import numpy as np #####################
import pylab as plb
import dask.dataframe as dd
plb.rcParams['font.size'] = 20
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 100
plt.rcParams["figure.autolayout"] = True
st.set_page_config(page_title='Censo da Educação Superior no Brasil', page_icon=':bar_chart:', initial_sidebar_state='auto')

# Carregando a base de dados
@st.cache(allow_output_mutation=True, ttl=24*3600)
def load_data():
    df = dd.read_parquet('https://github.com/ginoidelatina/App-Web-Streamlit-microdados-INEP/blob/d1a92afa57e01b96be6f529aa3de9bb6ec9c2a00/dados/microdados2021-INEP.parquet?raw=true')    
    return df

def cursoSelect(userOptions): # Fitro de pesquisa de acordo com o nome do curso
    cursos = userOptions.compute().unique()
    cursos = cursos.tolist()
    cursos.sort()
    cursos.insert(0,'')
    curso_select = ''
    st.write('')
    curso_select = st.selectbox('Selecione o curso', options = cursos, key = 'ies04', help='ABI (Área Básica de Ingresso')
    st.write('')
    if curso_select == '':
        st.stop()
    else:
        del cursos
        return curso_select

def iesSelect(df): # Filtro de pesquisa de acordo com o nome da instituição
    nome_ies = df.compute().unique()
    nome_ies = nome_ies.tolist()
    nome_ies.sort()
    nome_ies.insert(0,'')
    nome_ies_select = ''
    st.write('')
    nome_ies_select = st.selectbox('Selecione o nome da instituição', options = nome_ies,key='rs03')
    st.write('')
    if nome_ies_select == '':
       st.stop() 
    else:
        del nome_ies
        return nome_ies_select

# Campos selecionados pelo usuário.
def userSelect(dataframe, uf_select, adm_select, pesquisar_curso, pesquisar_ies):
    dataframe = dataframe
    
    # Dicionário para os registros do campo 'TP_CATEGORIA_ADMINISTRATIVA'.
    dic_TP_CATEGORIA_ADMINISTRATIVA = {
    'Pública Federal':1,
    'Pública Estadual':2,
    'Pública Municipal':3,
    'Privada com fins lucrativos':4,
    'Privada sem fins lucrativos':5}

    if uf_select == 'Todas opções' and adm_select == 'Todas opções':
        if pesquisar_curso == 'Não':
            df = dataframe.compute()
            return df, True
        else:
            df_temp = dataframe['NO_CURSO']
            nome_curso = cursoSelect(df_temp)
            df = dataframe[dataframe.NO_CURSO == nome_curso]
            df = df.compute()

            del df_temp, nome_curso
            return df, True
            

    if uf_select == 'Todas opções' and adm_select != 'Todas opções':
        df = dataframe.loc[dataframe.TP_CATEGORIA_ADMINISTRATIVA == dic_TP_CATEGORIA_ADMINISTRATIVA[adm_select]]
        df = df.drop(['TP_CATEGORIA_ADMINISTRATIVA', 'SG_UF_IES', 'NO_IES'], axis=1)
        if pesquisar_curso == 'Não':
            df = df.drop('NO_CURSO', axis=1)
            df = df.compute().dropna()
            return df, True

        else:
            df_temp = df['NO_CURSO']
            nome_curso = cursoSelect(df_temp)
            df = df.loc[df.NO_CURSO == nome_curso]
            df = df.drop('NO_CURSO', axis=1)
            df = df.compute().dropna()
            del df_temp, nome_curso
            return df, True

    if uf_select != 'Todas opções' and adm_select == 'Todas opções':
        df = dataframe.loc[dataframe.SG_UF_IES == uf_select]
        if pesquisar_ies == 'Não':
            df = df.drop(['TP_CATEGORIA_ADMINISTRATIVA', 'SG_UF_IES', 'NO_IES'], axis=1)
            if pesquisar_curso == 'Não':
                df = df.drop('NO_CURSO', axis=1)
                df = df.compute().dropna()
                return df, True
            else:
                df_temp = df['NO_CURSO']
                nome_curso = cursoSelect(df_temp)
                df = df.loc[df.NO_CURSO == nome_curso]
                df = df.drop('NO_CURSO', axis=1)
                df = df.compute().dropna()
                del df, nome_curso
                return df, True


        if pesquisar_ies == 'Sim':
            if pesquisar_curso == 'Não':
                df = df.drop(['TP_CATEGORIA_ADMINISTRATIVA', 'SG_UF_IES'], axis=1)
                df_temp = df['NO_IES']
                nome_ies = iesSelect(df_temp)
                df = df.loc[df.NO_IES == nome_ies]
                df = df.drop(['NO_IES', 'NO_CURSO'], axis=1)
                df = df.compute().dropna()
                del df_temp, nome_ies
                return df, True

    
            else:
                df_temp = df['NO_IES']
                nome_ies = iesSelect(df_temp)
                df = df.loc[df.NO_IES == nome_ies]
                nome_curso = cursoSelect(df.NO_CURSO)
                df = df.loc[df.NO_CURSO == nome_curso]
                df = df.drop(['TP_CATEGORIA_ADMINISTRATIVA', 'SG_UF_IES', 'NO_IES', 'NO_CURSO'], axis=1)
                df = df.compute().dropna()
                del df_temp, nome_ies, nome_curso
                return df, True


    if uf_select != 'Todas opções' and adm_select != 'Todas opções':
        df = dataframe.loc[dataframe.SG_UF_IES== uf_select]
        df = df.loc[df.TP_CATEGORIA_ADMINISTRATIVA == dic_TP_CATEGORIA_ADMINISTRATIVA[adm_select]]
        if pesquisar_ies == 'Não':
            df = df.drop(['TP_CATEGORIA_ADMINISTRATIVA', 'SG_UF_IES', 'NO_IES'], axis=1)
            if pesquisar_curso == 'Não':
                df.drop('NO_CURSO', axis=1)
                df = df.compute().dropna()
                return df, True
            else:
                df_temp = df['NO_CURSO']
                nome_curso = cursoSelect(df_temp)
                df = df.loc[df.NO_CURSO == nome_curso]
                df = df.drop('NO_CURSO', axis=1)
                df = df.compute().dropna()
                del df_temp, nome_curso
                return df, True

        if pesquisar_ies == 'Sim':
            df = df.drop(['TP_CATEGORIA_ADMINISTRATIVA', 'SG_UF_IES'], axis=1)
            if pesquisar_curso == 'Não':
                df_temp = df['NO_IES']
                nome_ies = iesSelect(df_temp)
                df = df.loc[df.NO_IES == nome_ies]
                df = df.drop(['NO_IES', 'NO_CURSO'], axis=1)
                df = df.compute().dropna()
                del df_temp, nome_ies
                return df, True
            else:
                df_temp = df['NO_IES']
                nome_ies = iesSelect(df_temp)
                df = df.loc[df.NO_IES == nome_ies]
                nome_curso = cursoSelect(df.NO_CURSO)
                df = df.loc[df.NO_CURSO == nome_curso]
                df = df.drop(['NO_IES', 'NO_CURSO'], axis=1)
                df = df.compute().dropna()
                return df, True

def selected_attributes():
    st.write('Selecione os atributos que deseja analisar')
    checkboxCorRaca = st.checkbox('Cor ou raça')
    checkboxGenero = st.checkbox('Gênero')
    checkboxIdade = st.checkbox('Idade')
    checkboxEnsinoMedio = st.checkbox('Tipo de escola que terminaram o ensino médio')
    checkboxPCDTGD = st.checkbox('Portabilidade de deficiência, transtorno global do desenvolvimento ou altas habilidades')

    options = list([checkboxCorRaca, checkboxGenero, checkboxIdade, checkboxEnsinoMedio, checkboxPCDTGD])
    
    st.write('')
    button = st.button('Buscar')
    st.write('')
    if (button != True):
        st.stop()
    if (button == True) and (True in options):
        return options, button

def plotResults(datafiltred, selected_attributes):
        if (selected_attributes[0] == True):
            dataCorRaca(datafiltred)
        if (selected_attributes[1] == True):
            dataGenero(datafiltred)
        if (selected_attributes[2] == True):
            dataIdade(datafiltred)
        if (selected_attributes[3] == True):
            dataEscolaridade(datafiltred)
        if (selected_attributes[4] == True):
            dataPCD(datafiltred)
        st.info('Para este projeto utilizamos um ciclo de cores amigável para deficiência de visão de cores.\
                As cores selecionadas mostram-se razoavelmente bem em filtros daltônicos (embora não em monocromático puro). \
                Para tornar a interpretação dos gráficos mais precisa e acessível, também aplicamos diferentes marcadores para plotar os dados, tais como \
                formas geométricas (círculos, estrelas e quadrados), bem como diferentes estilos de linhas (linhas sólidas, tracejadas, pontilhadas). \
                Caso tenha interesse em verificar as fontes de cores e os marcadores utilizados, basta acessar o Github deste projeto.', icon='ℹ️')


 
# Plotagem dos gráficos
def plotBar(dataframe, hatches, suptitle):
    CB_color  = ['#377eb8', '#e41a1c' , '#4daf4a',\
    '#f781bf', '#a65628' , '#984ea3',\
        '#999999' , '#e41a1c' , '#dede00']


    dataframe = dataframe
    result_pct = dataframe.div(dataframe.sum(1), axis=0)
    ax = result_pct.plot(kind='bar', align='center',figsize=(14,7), width=3, edgecolor='black', color=CB_color) #sharex=True, sharey=y  figsize=(10,6)
    bars = ax.patches
    hatches = hatches
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)

    plt.legend(labels=dataframe.columns, loc='best', bbox_to_anchor=(1.1, 1.05), fontsize= 'large') #loc='best' bbox_to_anchor=(1.1, 1.05)
    plt.suptitle(suptitle, fontsize='x-large', y=0.98)
    plt.xticks(fontsize='large',fontweight='light') 
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    plt.yticks([])

    for p in ax.patches:
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy() 
        ax.annotate('{:.00001%}'.format(height), (p.get_x()+.5*width, p.get_y() + height + 0.01), ha = 'center')
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='#EEEEEE')
    ax.xaxis.grid(False)

    buf = BytesIO()
    plt.savefig(buf, format='png') #format="png", 
    plt.tight_layout(True)
    st.image(buf, use_column_width=True) #use_column_width=True
    plt.clf()
    return 
        
def plotPie(values, labels, subtitle):
    colors = ['#dede00','#e41a1c', '#999999']
    fig, ax = plt.subplots(figsize=(14,7))
    ax.pie(values, autopct='%1.1f%%', shadow=False, startangle=60, pctdistance=0.5, colors=colors)  ####### shadow = False
    fig.suptitle(subtitle, fontsize='x-large')
    ax.axis('equal')
    plt.legend(labels=labels, loc='best', fontsize = 'large', bbox_to_anchor=(1.1, 1.05)) #
    plt.xticks(fontsize='large',fontweight='light')
    
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.tight_layout(True)
    st.image(buf, use_column_width=True)    #st.pyplot(plt) 
    plt.clf()

    return 


def plotLine(x, y, subtitle):
    plt.figure(tight_layout=True, figsize=(18,14))#fillstyle = 'full') figsize=(16,12))
    plt.plot(x, y, linestyle='-', marker='o', linewidth=3, markersize=16, dash_capstyle='round', color='#e41a1c')
    plt.ylabel('Quantidade de alunos', fontweight='light', fontsize = 'large') 
    plt.grid(True)
    plt.xticks(rotation=60,fontweight='light', ha='center', fontsize='large')
    plt.suptitle(subtitle, fontsize='x-large')
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.tight_layout(True)
    st.image(buf, use_column_width=True)
    plt.clf()
    return 

def dataCorRaca(dataframe):
    with st.container():
        st.subheader('Dados relativos à cor e raça')

        # Manipulando atributos relacionados à cor e raça
        columns = ['Não declarado', 'Branca','Preta', 'Parda', 'Amarela', 'Indígena']
        values = [[dataframe['QT_MAT_CORND'].sum(), dataframe['QT_MAT_BRANCA'].sum(),\
            dataframe['QT_MAT_PRETA'].sum(), dataframe['QT_MAT_PARDA'].sum(), dataframe['QT_MAT_AMARELA'].sum(),\
                dataframe['QT_MAT_INDIGENA'].sum()]]

        data = pd.DataFrame(values, columns=columns) 
        
        # PLOTAR GRÁFICO TIPO BARRA
        hatches = ('//', '.', '*', 'o', 'xx','++')
        subtitle = 'Percentual de alunos, por cor ou raça'
        plotBar(data, hatches, subtitle)

        # PLOTAR TABELAS
        with st.expander('Veja a tabela'):
            #st.code('Quantidade de alunos por raça ou cor')
            data['Total de alunos'] = np.sum(values)
            data = data.stack(0)
            data.rename('Quantidade de alunos', axis='columns', inplace=True)
            data.reset_index(level=0, drop=True, inplace=True)
            data.rename({'level_1':'Idade dos alunos'}, inplace=True)
            st.table(data)
        del columns, values, data, hatches, subtitle

    st.write('') 
    st.write('') 
    st.write('') 
    return None

def dataGenero(dataframe):
    with st.container():
        st.subheader('Dados relativos à gênero')

        # Manipulando atributos relacionados à cor e raça
        values = [dataframe['QT_MAT_FEM'].sum(), dataframe['QT_MAT_MASC'].sum()]
        labels = ['Feminino', 'Masculino']
        data = pd.DataFrame([values], columns=labels)

        # PLOTAR GRÁFICO TIPO PIZZA
        subtitle = 'Percentual de alunos, por gênero'
        plotPie(values, labels, subtitle)
        st.warning('O Censo da Educação Superior coletou apenas gêneros binários.', icon='⚠️')
        
        # PLOTAR TABELAS
        with st.expander('Veja a tabela'):
            #st.code("Quantidade de alunos por gênero")
            data['Total de alunos'] = np.sum(values)
            data = data.stack(0)
            data.rename('Quantidade de alunos', axis='columns', inplace=True)
            data.reset_index(level=0, drop=True, inplace=True)
            data.rename({'level_1':'Idade dos alunos'}, inplace=True)
            st.table(data)
        del values, labels, data, subtitle

    st.write('')
    st.write('') 
    st.write('') 
    return None

def dataIdade(dataframe):
    with st.container():
        st.subheader('Dados relativos à idade') #st.subheader('Quantidade de matriculados por idade')

        # Manipulando atributos relacionados à idade
        # Eixo x
        columns = ['Até 17 anos de idade', 'De 18 a 24 anos de idade', ' De 25 a 29 anos de idade', 'De 30 a 34 anos de idade',\
            'De 35 a 39 anos de idade', 'De 40 a 49 anos de idade', 'De 50 a 59 anos de idade', 'De 60 ou mais anos de idade']

        # Eixo Y
        values = [dataframe['QT_MAT_0_17'].sum(), dataframe['QT_MAT_18_24'].sum(),\
            dataframe['QT_MAT_25_29'].sum(), dataframe['QT_MAT_30_34'].sum(), dataframe['QT_MAT_35_39'].sum(),\
                dataframe['QT_MAT_40_49'].sum(), dataframe['QT_MAT_50_59'].sum(), dataframe['QT_MAT_60_MAIS'].sum()]
        data = pd.DataFrame([values], columns=columns) 
        
        
        tab1, tab2 = st.tabs(['Gráfico em linha', 'Gráfico em barra'])
        # PLOTAR GRÁFICO TIPO LINHA
        with tab1:
            subtitle = 'Quantidade de alunos por classe etária'
            plotLine(columns, values, subtitle)
            del subtitle
        # PLOTAR GRÁFICO TIPO BARRA
        with tab2:
            hatches = ('//', '.', '*', 'o', 'xx','++', '-', '|')
            subtitle = 'Percentual de alunos, por classe etária'
            plotBar(data, hatches, subtitle)


        # PLOTAR TABELAS
        with st.expander('Veja a tabela'):
            data = data.stack(0)
            data.rename('Quantidade de alunos', axis='columns', inplace=True)
            data.reset_index(level=0, drop=True, inplace=True)
            data.rename({'level_1':'Idade dos alunos'}, inplace=True)
            st.write(data)

            st.warning(
            'É possível ordenar as classes etárias dos alunos por frequência de ocorrência.\
            Para isso, basta clicar (ou apertar) em cima da coluna "Quantidade de alunos",\
            até aparecer o tipo de ordenação desejada.\
            ', icon='⚠️')
        del columns, values, data, hatches, subtitle
        
    st.write('') 
    st.write('') 
    st.write('') 
    return None

def dataEscolaridade(dataframe):
    with st.container():
        st.subheader('Dados relativos ao tipo de escola frequentada pelos alunos durante o ensino médio')
        
        # Manipulando atributos relacionados ao tipo a escoloridade do ensino médio
        columns = ['Alunos que terminaram\n o ensino médio em\n escolas públicas',\
            'Alunos que terminaram\n o ensino médio em\n escolas privadas',\
                'Alunos que não informaram\n o tipo de escola que\n terminaram o ensino médio']
        values = [dataframe['QT_MAT_PROCESCPUBLICA'].sum(),  dataframe['QT_MAT_PROCESCPRIVADA'].sum(),\
                dataframe['QT_MAT_PROCNAOINFORMADA'].sum()]
        
        data = pd.DataFrame([values], columns=columns) 
        
        tab1, tab2 = st.tabs(['Gráfico em barra', 'Gráfico de setores'])
        
        # PLOTAR GRÁFICO TIPO BARRA
        with tab1:
            hatches = ('//', 'o', '++')
            suptitle = 'Percentual de alunos, por tipo de escola\nfrequentada durante o ensino médio'
            plotBar(data, hatches, suptitle)
        
        with tab2:
            # PLOTAR GRÁFICO TIPO PIZZA
            plotPie(values, columns, suptitle)

        # PLOTAR TABELAS
        with st.expander('Veja a tabela'):
            data['Total de alunos'] = np.sum(values)
            data = data.stack(0)
            data.rename('Quantidade de alunos', axis='columns', inplace=True)
            data.reset_index(level=0, drop=True, inplace=True)
            data.rename({'level_1':'Idade dos alunos'}, inplace=True)
            st.table(data)



        del columns, values, data, hatches, suptitle
        
    st.write('')
    st.write('') 
    st.write('') 
    return None

def dataPCD(dataframe):
    with st.container():
        st.subheader('Dados relativos à portabilidade de deficiência, transtorno global do desenvolvimento ou altas habilidades/superdotação')

        # Manipulando atributos relacionados ao tipo a escoloridade do ensino médio
        columns = ['Alunos com deficiência,\n transtorno global do\n desenvolvimento ou altas\n habilidades/superdotação', \
            'Alunos sem deficiência,\n transtorno global do\n desenvolvimento ou altas\n habilidades/superdotação']

        varNoDef = np.sum(np.abs(dataframe.QT_MAT.sum() - dataframe.QT_MAT_DEFICIENTE.sum()))

        values = [dataframe['QT_MAT_DEFICIENTE'].sum(), varNoDef]

        data = pd.DataFrame([values], columns=columns) 
        
        tab1, tab2 = st.tabs(['Gráfico em barra', 'Gráfico de setores'])
        # PLOTAR GRÁFICO TIPO BARRA
        with tab1:
            hatches = ('//', 'o', '++')
            hatches = ('//', 'o', '++')
            suptitle = 'Percentual de alunos com deficiência, transtorno global\n do desenvolvimento ou altas habilidades'
            plotBar(data, hatches, suptitle)
        with tab2:
            plotPie(values, columns, suptitle)

        st.warning('A descrição dos atributos acima foram retiradas do Censo da Educação Superior.', icon='⚠️')

        # PLOTAR TABELAS
        with st.expander('Veja a tabela'):
            data['Total de alunos'] = np.sum(values)
            data = data.stack(0)
            data.rename('Quantidade de alunos', axis='columns', inplace=True)
            data.reset_index(level=0, drop=True, inplace=True)
            data.rename({'level_1':'Idade dos alunos'}, inplace=True)
            st.table(data)
        del columns, values, data, hatches, suptitle, varNoDef

    st.write('') 
    st.write('') 
    st.write('') 
    return None 


 ###################################################################################################################################
    

# Exibição da página
def main():

    pd.set_option('max_colwidth', 400)


    dataframe = load_data()

    st.header('Visualização de dados do Censo da Educação Superior no Brasil')  

    with st.sidebar:
        st.title('Sobre')
        
        st.markdown(
            '<blockquote><p>Esta página web tem como objetivo partilhar estatísticas descritivas sobre o acesso à Educação Superior no Brasil.</p>\
            Para obter indicadores educacionais, acessíveis aos pesquisadores, estudantes, gestores e sociedade em geral, este presente instrumento\
            fornece representações visuais de dados para analisar quantitativamente a distribuição de alunos de acordo com atributos específicos.</blockquote>', unsafe_allow_html=True )

        st.write('') 
        st.write('') 
        st.write('')


        st.info('Este site utiliza os Microdados do Censo da Educação Superior, disponível pelo Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira\
            [(Inep)](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-da-educacao-superior)', icon='ℹ️')
            
        st.markdown('[![github](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/ginoidelatina/pi3-streamlitapp-microdadoINEP)</p></blockquote>', unsafe_allow_html=True)

    with st.container():
        colleft, colright = st.columns(2 , gap="large")
        with colright:
            st.success('Na barra lateral, selecione ao menos uma Unidade Federativa de seu interesse (sendo 26 estados e um distrito federal)\
                ou até mesmo todas Unidades Federativas do Brasil, basta selecionar "Todas opções".\
                Você também deve escolher o tipo de categoria administrativa (exemplos: universidades públicas ou privadas). \
                Se tiver interesse em analisar as universidades independentemente do tipo da categoria administrativa, então marque "Todas opções".')
                
            st.success(
                'Também é possível filtrar os dados pelo nome da Instituição de Ensino Superior (IES) ou nome do curso,\
                nos quais dependem dos filtros aplicados previamente.')
            st.success(
                'Após selecionar todos os filtros, escolha ao menos um dos cinco atributos que listados. Por fim, aperte botão "buscar", para obter as estatísticas agrupadas por segmentos\
                    específicos da população.')                       
                
            st.write('') 
            st.write('')
            st.write('')

    with colleft:
            st.subheader('Buscar gráficos')

            # Escolher o Estado
            uf = dataframe['SG_UF_IES']
            uf = uf.compute().unique()
            uf = uf.tolist()
            uf.sort()
            uf.insert(0,'')
            uf.insert(1,'Todas opções')
            uf_select = st.selectbox('Selecione a Unidade Federativa?', options = uf, key='uf01')
            del uf

            adm_select = st.selectbox('Selecione o tipo de categoria administrativa',\
                options = ['','Todas opções', 'Pública Federal', 'Pública Estadual', 'Pública Municipal', 'Privada com fins lucrativos', 'Privada sem fins lucrativos'], key='adm02')
            
            #disabled = True

            
            ########## vou precisar mudar o estado da sessão


            pesquisar_curso = st.selectbox('Deseja selecionar um curso específico?', options=['','Sim', 'Não'], key="disabled")
            #pesquisar_ies = st.selectbox("Deseja buscar os resultados pelo nome da instituição?",  ['','Sim', 'Não'], help='Para realizar a busca pelo nome da instituição, você deve escolher primeiro a unidade federativa que a contém.',key=2, disabled=True)

            # Iniciando as variáveis
            filterApplied = False
            button = None
            #del disabled
            if uf_select != '' and adm_select != '':
                if uf_select == 'Todas opções' and adm_select == 'Todas opções':
                    if (pesquisar_curso != ''):
                        st.write('') 
                        datafiltred, filterApplied = userSelect(dataframe, uf_select, adm_select, pesquisar_curso, pesquisar_ies='Não')
                        st.write('')
                        if filterApplied == True:
                            attributes, button = selected_attributes()

    
                if uf_select != 'Todas opções' or adm_select != 'Todas opções':
                    if pesquisar_curso != '':
                        pesquisar_ies = st.selectbox("Deseja buscar os resultados pelo nome da instituição?",  ['','Sim', 'Não'], key=2)
                        if pesquisar_ies != '':
                            st.write('')
                            datafiltred, filterApplied = userSelect(dataframe, uf_select, adm_select, pesquisar_curso, pesquisar_ies)
                            st.write('')
                            if filterApplied == True:
                                attributes, button = selected_attributes()
    st.write('') 
    st.write('')
    st.write('') 
    st.write('')
    st.write('')
    if button == True:
        plotResults(datafiltred, attributes)
   
    

        
main()
