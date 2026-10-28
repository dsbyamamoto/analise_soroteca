import pandas as pd
import plotly.express as px
from filtros_info import df_doenca_total, df_apenas_doencas, teste_rapido, teste_elisa, numero_diagnostico, df_contagem_geral, df_sexo_doenca

df = pd.read_csv("dados/dados_tratados/soroteca_tratada1.csv")

def bar_doenca_dup(df, doenca_alvo: str):
    """
    Gráfico de barras que retorna o número de amostras de acordo com a doença-alvo, para 
    avaliar o nº total de amostras e o nº de animais únicos com a doença escolhida para a
    análise.

    Args:
        df: é o dataframe geral;
        doenca_alvo: qualquer doença do dataframe.
    """

    dados = pd.DataFrame(
        {
            'Tipo': [f'Total com {doenca_alvo}', 
                     f'Apenas com {doenca_alvo}', 
                     f'Total com {doenca_alvo}', 
                     f'Apenas com {doenca_alvo}'],
            'Valores':[len(df_doenca_total(df, doenca_alvo, duplicata= 'sim')), 
                       len(df_apenas_doencas(df, doenca_alvo, duplicata= 'sim')), 
                       len(df_doenca_total(df, doenca_alvo, duplicata= 'não')), 
                       len(df_apenas_doencas(df, doenca_alvo, duplicata= 'não'))],
            'Categoria': ['c/Duplicata', 'c/Duplicata', 's/Duplicata', 's/Duplicata']
        }
    )

    fig = px.bar(
        data_frame= dados, 
        x='Categoria', 
        y='Valores', 
        color= 'Tipo', 
        title= f'Perfil de Cães com {doenca_alvo}',
        barmode= 'overlay',
        category_orders= {'Tipo': [f'Total com {doenca_alvo}', f'Apenas com {doenca_alvo}']},
        text_auto= True,
        width= 700,
        height= 600,
        opacity= 0.4
    )

    fig.update_xaxes(
                     showgrid= False,
                     showline= True,
                     linecolor= 'black',
                     linewidth= 2
                    )  

    fig.update_yaxes(
                     range= [0, 50],
                     showgrid= False,
                     showline= True,
                     linecolor= 'black',
                     linewidth= 2
                    )

    fig.update_traces( 
                    marker_line_color= '#000000',
                    marker_line_width= 2,
                    width= 0.6,
                    textfont_color= '#000000'
                    )

    fig.update_layout(
                    title= {'text': f'Perfil de Cães com {doenca_alvo}',
                            'font': {'size': 22},
                            'x': 0.5},
                    plot_bgcolor= '#FFFFFF'
                    )

    return fig

def bar_perfil_rapido(df):
    """ 
    Função que vai retornar um gráfico de barra com o perfil das amostras
    testadas por teste rápido, considerando os resultados (positivo, negativo 
    e sem resultado) por doença de interesse. 

    Args:
        df: é o dataframe geral.
    """

    df_rapido = pd.DataFrame({
        'erliquiose': {'positivo': teste_rapido(df, 'erliquiose', 'Positivo'), 
                       'negativo': teste_rapido(df,'erliquiose', 'Negativo'), 
                       'sem resultado': teste_rapido(df, 'erliquiose', 'Sem Resultado') 
                        },
        'babesiose':  {'positivo': teste_rapido(df, 'babesiose', 'Positivo'), 
                       'negativo': teste_rapido(df,'babesiose', 'Negativo'), 
                       'sem resultado': teste_rapido(df, 'babesiose', 'Sem Resultado') 
                        },
        'anaplasmose': {'positivo': teste_rapido(df, 'anaplasmose', 'Positivo'), 
                        'negativo': teste_rapido(df,'anaplasmose', 'Negativo'), 
                        'sem resultado': teste_rapido(df, 'anaplasmose', 'Sem Resultado') 
                        },
        'leishmaniose': {'positivo': teste_rapido(df, 'leishmaniose', 'Positivo'), 
                         'negativo': teste_rapido(df,'leishmaniose', 'Negativo'), 
                         'sem resultado': teste_rapido(df, 'leishmaniose', 'Sem Resultado') 
                         },
        'cinomose': {'positivo': teste_rapido(df, 'cinomose', 'Positivo'), 
                     'negativo': teste_rapido(df,'cinomose', 'Negativo'), 
                     'sem resultado': teste_rapido(df, 'cinomose', 'Sem Resultado') 
                    }
    })

    # as doenças de interesse viram índice
    df_rapido = df_rapido.T

    df_rapido = df_rapido.reset_index().melt(
        id_vars= 'index',
        var_name= 'Resultado',
        value_name= 'Quantidade' 
    ).sort_values(by= 'index')

    fig = px.bar(
        data_frame= df_rapido,
        barmode= 'group',
        x= 'index',
        y= 'Quantidade',
        color= 'Resultado',
        labels= {'index': 'Doença'},
        text_auto= True,
        width= 1000,
        height= 500
    )

    fig.update_xaxes(
                    showgrid= False,
                    showline= True,
                    linecolor= 'black',
                    linewidth= 2
                    )  

    fig.update_yaxes(
                    showgrid= False,
                    showline= True,
                    linecolor= 'black',
                    linewidth= 2
                    )

    fig.update_traces(textfont_color= '#000000')

    fig.update_layout(
        title= {'text': 'Perfil de Animais Testados: Teste Rápido',
                'font': {'size': 22},
                'x': 0.5},
        plot_bgcolor= '#FFFFFF'
    )

    return fig

def bar_perfil_elisa(df):
    """ 
    Função que vai retornar um gráfico de barra com o perfil das amostras
    testadas por sorologia, considerando os resultados por doença de interesse. 

    Args:
        df: é o dataframe geral.
    """

    df_elisa = pd.DataFrame({
        'erliquiose': {'(+) IgG': teste_elisa(df, 'erliquiose', '(+) IgG'),
                        '(+) IgM': teste_elisa(df, 'erliquiose', '(+) IgM'),
                        '(+) IgG e (+) IgM': teste_elisa(df, 'erliquiose', '(+) IgG e (+) IgM'),
                        '(+) IgG e/ou (+) IgM': teste_elisa(df, 'erliquiose', '(+) IgG e/ou (+) IgM'),
                        '(-) IgG e (-) IgM': teste_elisa(df, 'erliquiose', '(-) IgG e (-) IgM'),
                        'Sem Resultado': teste_elisa(df, 'erliquiose', 'Sem Resultado')
                        },
        'babesiose': {'(+) IgG': teste_elisa(df, 'babesiose', '(+) IgG'),
                    '(+) IgM': teste_elisa(df, 'babesiose', '(+) IgM'),
                    '(+) IgG e (+) IgM': teste_elisa(df, 'babesiose', '(+) IgG e (+) IgM'),
                    '(+) IgG e/ou (+) IgM': teste_elisa(df, 'babesiose', '(+) IgG e/ou (+) IgM'),
                    '(-) IgG e (-) IgM': teste_elisa(df, 'babesiose', '(-) IgG e (-) IgM'),
                    'Sem Resultado': teste_elisa(df, 'babesiose', 'Sem Resultado')
                        },
        'anaplasmose': {'(+) IgG': teste_elisa(df, 'anaplasmose', '(+) IgG'),
                        '(+) IgM': teste_elisa(df, 'anaplasmose', '(+) IgM'),
                        '(+) IgG e (+) IgM': teste_elisa(df, 'anaplasmose', '(+) IgG e (+) IgM'),
                        '(+) IgG e/ou (+) IgM': teste_elisa(df, 'anaplasmose', '(+) IgG e/ou (+) IgM'),
                        '(-) IgG e (-) IgM': teste_elisa(df, 'anaplasmose', '(-) IgG e (-) IgM'),
                        'Sem Resultado': teste_elisa(df, 'anaplasmose', 'Sem Resultado')
                        },
        'leishmaniose': {'(+) IgG': teste_elisa(df, 'leishmaniose', '(+) IgG'),
                        '(+) IgM': teste_elisa(df, 'leishmaniose', '(+) IgM'),
                        '(+) IgG e (+) IgM': teste_elisa(df, 'leishmaniose', '(+) IgG e (+) IgM'),
                        '(+) IgG e/ou (+) IgM': teste_elisa(df, 'leishmaniose', '(+) IgG e/ou (+) IgM'),
                        '(-) IgG e (-) IgM': teste_elisa(df, 'leishmaniose', '(-) IgG e (-) IgM'),
                        'Sem Resultado': teste_elisa(df, 'leishmaniose', 'Sem Resultado')
                        }
    })

    teste_elisa(df, doenca= 'erliquiose', resultado= 'Sem Resultado')
    df_elisa_t = df_elisa.T

    df_elisa_t = df_elisa_t.reset_index().melt(
        id_vars= 'index',
        var_name= 'Resultado',
        value_name= 'Quantidade'
    ).sort_values('index')

    fig = px.bar(
        data_frame= df_elisa_t,
        barmode= 'group',
        x= 'Quantidade',
        y= 'index',
        color= 'Resultado',
        orientation= 'h',
        labels= {'index': 'Doença'},
        text_auto= True,
        width= 900,
        height= 800
    )

    fig.update_xaxes(
                    showgrid= False,
                    showline= True,
                    linecolor= 'black',
                    linewidth= 2
                    )  

    fig.update_yaxes(
                    showgrid= False,
                    showline= True,
                    linecolor= 'black',
                    linewidth= 2
                    )

    fig.update_layout(
                      title= {'text': 'Perfil de Animais Testados: Sorologia',
                              'font': {'size': 22},
                              'x': 0.5},
                      plot_bgcolor= '#FFFFFF'
                    )

    return fig

def bar_teste_rapido_doenca(df, eixo_x= str):
    """
    Função que retorna um gráfico de barras sobre animais que testaram com teste rápido 
    para a doença determinada pelo argumento "eixo_x".

    Args:
        df: é o dataframe geral;
        eixo_x: seria a coluna da planilha de origem que diz sobre a doença e o teste utilizado, 
                exemplo ('leishmaniose_ELISA').
    """
    
    # filtrando cães que fizeram teste rápido para a doença determinada pelo eixo X
    resultados = ['Sem Resultado', 'Positivo', 'Negativo']
    df[eixo_x] = pd.Categorical(df[eixo_x], categories = resultados)
    df = df[eixo_x].value_counts(sort= False).reset_index()
    df.columns = ['resultado', 'contagem']
    nome_doença = eixo_x.split('_')
    nome_doença = nome_doença[0]

    fig = px.bar(
                df,
                x= 'resultado',
                y= 'contagem',
                color= 'resultado',
                color_discrete_map= {'Sem Resultado': '#F7F66A', 'Positivo': '#6FB562', 'Negativo': '#D92914'},
                labels= {'resultado': 'Resultado', 'contagem': 'n° de animais'},
                text_auto= True
                )

    fig.update_xaxes(
                    showgrid= False,
                    showline= True,
                    linecolor= 'black',
                    linewidth= 2,
                    type= 'category',
                    categoryorder= 'array',
                    categoryarray= resultados
                    )  

    fig.update_yaxes(
                    showgrid= False,
                    showline= True,
                    linecolor= 'black',
                    linewidth= 2
                    )
    
    fig.update_layout(title= {'text': f'Cães Testados para {nome_doença} com Teste Rápido e seus Resultados',
                              'font': {'size': 15}},
                      showlegend= False
                    )

    return fig 

def bar_sorologia_doenca(df, eixo_x= str):
    """
    Função que retorna um gráfico de barras sobre animais que testaram com sorologia 
    para a doença determinada pelo argumento "eixo_x"

    Args:
        df: é o dataframe geral;
        eixo_x: seria a coluna da planilha de origem que diz sobre a doença e o teste utilizado, 
                exemplo ('leishmaniose_ELISA').
    """
    
    # filtrando cães que fizeram sorologia para a doença determinada pelo eixo X
    resultados = ['Sem Resultado', '(+) IgG', '(+) IgM', '(+) IgG e (+) IgM', '(+) IgG e/ou (+) IgM', '(-) IgG e (-) IgM']
    df[eixo_x] = pd.Categorical(df[eixo_x], categories= resultados)
    df = df[eixo_x].value_counts(sort= False).reset_index()
    df.columns = ['resultado', 'contagem']
    nome_doença = eixo_x.split('_')
    nome_doença = nome_doença[0]

    # cães que fizeram teste rápido para determinada doença
    fig = px.bar(
                df,
                x= 'resultado',
                y= 'contagem',
                color= 'resultado',
                labels= {'resultado': 'Resultado', 'contagem': 'n° de animais'},
                text_auto= True
                )

    fig.update_xaxes(
                    showgrid= False,
                    showline= True,
                    linecolor= 'black',
                    linewidth= 2
                    )  

    fig.update_yaxes(
                    showgrid= False,
                    showline= True,
                    linecolor= 'black',
                    linewidth= 2
                    )
    
    fig.update_layout(
                    title= {'text': f'Cães Testados para {nome_doença} com Sorologia e seus Resultados',
                            'font': {'size': 15}},
                    showlegend= False  
                    )
    
    return fig 

def pie_total_doentes(df, doenca= str, cor_doenca= str, cor_total= str):
    """
    Função que vai gerar um pie chart da doença alvo, mostrando o número de acometidos
    em relação ao total de amostras cadastrados na planilha.

    Args:
        df: é o dataframe geral;
        doenca: doença de interesse entre "Erliquiose", "Babesiose", "Anaplasmose", 
               "Leishmaniose", "Cinomose" e "Leptospirose";
        cor_doenca: cor em # para indicar amostras acometidas pela doença;
        cor_total: cor em # para amostras não acometidas pela doença.
    """
    
    # apenas_doenca vai ter o número total de animais diagnosticados com 'doenca'
    com_doenca = df[df['diagnostico_final'].apply(lambda x: doenca in x)]
    # df_doenca é o dataframe que vai resumir os dados e comparar com o número total de animais do estudo
    df_doenca = pd.DataFrame({
        'referência': ['cães acometidos', 'nº de cães não afetados'],
        'valores': [len(com_doenca), (len(df) - len(com_doenca))]}
    )

    # criação de um pie chart para ter uma noção das proporções
    fig = px.pie(
                df_doenca,
                values= 'valores',
                names= 'referência',
                color= 'referência',
                color_discrete_map= {
                    'cães acometidos': cor_doenca,
                    'nº de cães não afetados': cor_total 
                },
                hole= .3
                )

    fig.update_layout(
                    title= {'text': f'Proporção de cães com {doenca} x total de cães', 
                            'font': {'size': 15}}
                    )

    fig.update_traces(texttemplate= '%{percent:.2%}')

    return fig

def pie_sexo(df, doenca_alvo= None):
    """
    Função que retorna um Pie Chart com base no gênero das amostras, podendo ou não filtrar
    por uma determinada categoria de doença.

    Args:
        df: é o dataframe geral;
        doenca_alvo: qualquer doença do dataframe.
    """

    if doenca_alvo != None:
        femea = df_sexo_doenca(df, doenca= doenca_alvo, sexo= "Fêmea")
        macho = df_sexo_doenca(df, doenca= doenca_alvo, sexo= 'Macho')
    else:
        femea = df[df['sexo'] == 'Fêmea']
        macho = df[df['sexo'] == 'Macho']

    df = pd.DataFrame({
            'sexo': ['Fêmea', 'Macho'],
            'valores': [len(femea), len(macho)]
        })
    
    # criação de um pie chart para ter uma noção das proporções
    fig = px.pie(
                df,
                values= 'valores',
                names= 'sexo',
                color= 'sexo',
                color_discrete_map= {
                    'Fêmea': '#FFB1CB',
                    'Macho': '#01A6EA' 
                    },
                hole= .3
                )

    fig.update_layout(
                    title= {'text': f'Proporção de cães Machos x Fêmeas', 
                            'font': {'size': 15}}
                    )

    fig.update_traces(texttemplate= '%{percent:.2%}')

    return fig

def hist_idade(df, doenca= None):
    """
    Função que retorna um histograma dos animais acometidos por determinada doença
    distribuídos por faixa etária. Se não for fornecido o argumento para doença, vai
    retornar um histograma geral das amostras, filtrando os animais pelo código

    Args:
        df: é o dataframe geral;
        doenca: doença de interesse entre "Erliquiose", "Babesiose", "Anaplasmose", 
               "Leishmaniose", "Cinomose" e "Leptospirose";
    """

    if doenca is not None:
        # filtrando cães acometidos pela doença selecionada
        df = df[df['diagnostico_final'].apply(lambda linha: doenca in linha)]
    
    # histograma da doença distribuído por faixa etária
    fig = px.histogram(
                    data_frame= df,
                    x= df['idade_aproximada_anos'],
                    color= df['sexo'],
                    color_discrete_map= {'Macho': '#01A6EA', 'Fêmea': '#FFB1CB'},
                    marginal= 'box',
                    nbins= 10
                    )

    fig.update_traces(
                    notched= False,
                    selector= dict(type= 'box')
                    )

    fig.update_xaxes(title_text= 'Faixa Etária')
    fig.update_xaxes(title_text='', row=2, col=1)

    fig.update_yaxes(title_text= 'Contagem')
    fig.update_yaxes(title_text='', row=2, col=1)

    if doenca is not None:
        fig.update_layout(
                        title= {'text': f"Distribuição de Cães com {doenca} por Faixa Etária (considerando o sexo)",
                                'font': {'size': 15}}
                        )
    else:
        fig.update_layout(
                        title= {'text': f"Distribuição de Cães por Faixa Etária (considerando o sexo)",
                                'font': {'size': 15}}
                        )

    return fig

def bar_geral(df):
    """
    Função que retorna gráfico com perfil geral de todas as categorias
    de doenças consideradas no estudo.

    Args:
        df: é o dataframe geral.
    """

    df_geral = df_contagem_geral(df)

    # Filtro para destacar as doenças de interesse. Transformando em lista para pegar o Index de cada uma
    df_filtro = df_geral
    df_filtro = df_filtro['Doença']
    df_filtro = df_filtro.to_list()

    fig = px.bar(
            data_frame= df_geral,
            x= 'Quantidade',
            y= 'Doença',
            orientation= 'h',
            text_auto= True,
            width= 1200,
            height= 800
        )
    
    fig.update_xaxes(
                     showgrid= False,
                     showline= True,
                     linecolor= 'black',
                     linewidth= 2
                     )  
    
    fig.update_yaxes(
                     showgrid= False,
                     showline= True,
                     linecolor= 'black',
                     linewidth= 2
                     )
    
    fig.update_layout(
                    title= {'text': 'Perfil de Diagnóstico',
                            'font': {'size': 15}}
                    )

    # Reseta o index para deixar em ordem
    df_geral = df_geral.reset_index().drop(columns= 'index')

    # Pega os índices de cada doença, usando a lista anterior para filtrar
    doencas_index = [
                    df_geral.loc[df_filtro.index('Erliquiose'), 'Doença'],
                    df_geral.loc[df_filtro.index('Babesiose'), 'Doença'],
                    df_geral.loc[df_filtro.index('Leishmaniose'), 'Doença'],
                    df_geral.loc[df_filtro.index('Anaplasmose'), 'Doença'],
                    df_geral.loc[df_filtro.index('Cinomose'), 'Doença']
                    ]

    # Cores estabelecidas para cada coluna
    cor_barras = ["#D52323" if linha in doencas_index else "#555252" for linha in df_filtro]
    
    fig.update_traces(
        marker_color= cor_barras
    )
    
    return fig

def bar_geral_sexo(df):
    """
    Função que retorna gráfico com perfil geral de todas as categorias
    de doenças consideradas no estudo, considerando o sexo

    Args:
        df: é o dataframe geral.
    """

    df_geral_sexo = pd.DataFrame({
        'Tumor': {'Macho': numero_diagnostico(df, 'Tumor', 'Macho'),
                'Fêmea': numero_diagnostico(df, 'Tumor', 'Fêmea')},
        'Erliquiose': {'Macho': numero_diagnostico(df, 'Erliquiose', 'Macho'),
                    'Fêmea': numero_diagnostico(df, 'Erliquiose', 'Fêmea')},
        'Babesiose': {'Macho': numero_diagnostico(df, 'Babesiose', 'Macho'),
                    'Fêmea': numero_diagnostico(df, 'Babesiose', 'Fêmea')},
        'Leishmaniose': {'Macho': numero_diagnostico(df, 'Leishmaniose', 'Macho'),
                        'Fêmea': numero_diagnostico(df, 'Leishmaniose', 'Fêmea')},
        'Leptospirose': {'Macho': numero_diagnostico(df, 'Leptospirose', 'Macho'),
                        'Fêmea': numero_diagnostico(df, 'Leptospirose', 'Fêmea')},
        'Cinomose': {'Macho': numero_diagnostico(df, 'Cinomose', 'Macho'),
                    'Fêmea': numero_diagnostico(df, 'Cinomose', 'Fêmea')},
        'Anaplasmose': {'Macho': numero_diagnostico(df, 'Anaplasmose', 'Macho'),
                        'Fêmea': numero_diagnostico(df, 'Anaplasmose', 'Fêmea')},
        'Doença de Chagas': {'Macho': numero_diagnostico(df, 'Doença de Chagas', 'Macho'),
                            'Fêmea': numero_diagnostico(df, 'Doença de Chagas', 'Fêmea')},
        'Otite': {'Macho': numero_diagnostico(df, 'Otite', 'Macho'),
                'Fêmea': numero_diagnostico(df, 'Otite', 'Fêmea')},
        'Doença urológica/renal': {'Macho': numero_diagnostico(df, 'Doença urológica/renal', 'Macho'),
                                'Fêmea': numero_diagnostico(df, 'Doença urológica/renal', 'Fêmea')},
        'Doença dermatológica': {'Macho': numero_diagnostico(df, 'Doença dermatológica', 'Macho'),
                                'Fêmea': numero_diagnostico(df, 'Doença dermatológica', 'Fêmea')},
        'Doença odontológica': {'Macho': numero_diagnostico(df, 'Doença odontológica', 'Macho'),
                                'Fêmea': numero_diagnostico(df, 'Doença odontológica', 'Fêmea')},
        'Doença ocular': {'Macho': numero_diagnostico(df, 'Doença ocular', 'Macho'),
                        'Fêmea': numero_diagnostico(df, 'Doença ocular', 'Fêmea')},
        'Doença respiratória': {'Macho': numero_diagnostico(df, 'Doença respiratória', 'Macho'),
                                'Fêmea': numero_diagnostico(df, 'Doença respiratória', 'Fêmea')},
        'Doença periodontal': {'Macho': numero_diagnostico(df, 'Doença periodontal', 'Macho'),
                            'Fêmea': numero_diagnostico(df, 'Doença periodontal', 'Fêmea')},
        'Doença endócrina': {'Macho': numero_diagnostico(df, 'Doença endócrina', 'Macho'),
                            'Fêmea': numero_diagnostico(df, 'Doença endócrina', 'Fêmea')},
        'Doença reprodutiva': {'Macho': numero_diagnostico(df, 'Doença reprodutiva', 'Macho'),
                            'Fêmea': numero_diagnostico(df, 'Doença reprodutiva', 'Fêmea')},
        'Doença gastrointestinal': {'Macho': numero_diagnostico(df, 'Doença gastrointestinal', 'Macho'),
                                    'Fêmea': numero_diagnostico(df, 'Doença gastrointestinal', 'Fêmea')},
        'Doença cardiovascular': {'Macho': numero_diagnostico(df, 'Doença cardiovascular', 'Macho'),
                                'Fêmea': numero_diagnostico(df, 'Doença cardiovascular', 'Fêmea')},
        'Doença musculoesquelética': {'Macho': numero_diagnostico(df, 'Doença musculoesquelética', 'Macho'),
                                    'Fêmea': numero_diagnostico(df, 'Doença musculoesquelética', 'Fêmea')},
        'Outros': {'Macho': numero_diagnostico(df, 'Outros', 'Macho'),
                'Fêmea': numero_diagnostico(df, 'Outros', 'Fêmea')},
        'Inconclusivo': {'Macho': numero_diagnostico(df, 'Inconclusivo', 'Macho'),
                        'Fêmea': numero_diagnostico(df, 'Inconclusivo', 'Fêmea')},
        'Doença neurológica': {'Macho': numero_diagnostico(df, 'Doença neurológica', 'Macho'),
                            'Fêmea': numero_diagnostico(df, 'Doença neurológica', 'Fêmea')}
    })

    df_geral_sexo = df_geral_sexo.T.reset_index().melt(
        id_vars= 'index',
        var_name= 'Sexo',
        value_name= 'Quantidade'
    ).sort_values(by= ['Quantidade'])

    fig = px.bar(
        data_frame= df_geral_sexo,
        x= 'Quantidade',
        y= 'index',
        color= 'Sexo',
        color_discrete_map= {'Macho': '#01A6EA', 'Fêmea': '#FFB1CB'},
        orientation= 'h',
        labels= {'index': 'Doenças'},
        text_auto= True,
        width= 1200,
        height= 800
    )

    fig.update_xaxes(
                    showgrid= False,
                    showline= True,
                    linecolor= 'black',
                    linewidth= 2
                    )  

    fig.update_yaxes(
                    showgrid= False,
                    showline= True,
                    linecolor= 'black',
                    linewidth= 2
                    )

    fig.update_layout(
                    title= {'text': 'Perfil de Diagnóstico por Sexo',
                            'font': {'size': 15}}
                    )

    return fig

def bar_animais_raca(df):
    """
    Função que retorna gráfico com o número de amostras por grupo de raça

    Args:
        df: é o dataframe geral.
    """

    df_raca = df['raça'].dropna()

    grupo_raca = {'SRD': 'SRD',
                'Yorkshire': 'Pequeno Porte',
                'Shih Tzu': 'Braquiocefálico',
                'Pinscher': 'Pequeno Porte',
                'Pit Bull': 'Médio Porte',
                'Poodle': 'Pequeno Porte',
                'Lhasa Apso': 'Pequeno Porte',
                'Maltês': 'Pequeno Porte',
                'Bulldog Francês': 'Braquiocefálico',
                'Pastor Alemão': 'Grande Porte',
                'Lulu da Pomerânia': 'Pequeno Porte',
                'Labrador': 'Grande Porte',
                'Golden Retriever': 'Grande Porte',
                'Pug': 'Braquiocefálico',
                'Border Collie': 'Grande Porte',
                'Chow Chow': 'Médio Porte',
                'Spitz Alemão': 'Pequeno Porte',
                'Basset Hound': 'Médio Porte',
                'Cocker Spaniel': 'Médio Porte',
                'Dachshund': 'Pequeno Porte',
                'Husky Siberiano': 'Médio Porte',
                'Spitz': 'Pequeno Porte',
                'Blue Hiller': 'Médio Porte',
                'Boxer': 'Braquiocefálico',
                'Outro': 'SRD',
                'Rottweiler': 'Grande Porte',
                'Schnauzer Miniatura': 'Pequeno Porte',
                'Australian Cattle Dog': 'Médio Porte',
                'Cane Corso': 'Grande Porte',
                'Chihuahua': 'Pequeno Porte',
                'Fila Brasileiro': 'Grande Porte',
                'Fox Paulistinha': 'Médio Porte',
                'Beagle': 'Médio Porte',
                'Chihuaha Pelo Longo': 'Pequeno Porte',
                'Fila': 'Grande Porte',
                'Jack Russel': 'Pequeno Porte'
                }

    df_raca = df_raca.value_counts()
    df_raca = pd.DataFrame(df_raca)
    df_raca = df_raca.reset_index()
    df_raca['Grupos'] = df_raca['raça'].map(grupo_raca)
    df_raca.sort_values('Grupos')
    df_raca = df_raca.drop(columns = ['raça'])
    df_raca = df_raca.groupby(['Grupos']).sum().sort_values(by= 'count', ascending= False)
    df_raca = df_raca.reset_index()

    fig = px.bar(
        data_frame= df_raca,
        x= 'Grupos',
        y= 'count',
        labels= {'count': 'Quantidade'},
        text_auto= True,
        color_discrete_sequence= ['#97a6c4'] * 5,
    )

    fig.update_xaxes(
                    showgrid= False,
                    showline= True,
                    linecolor= 'black',
                    linewidth= 2
                    )  

    fig.update_yaxes(
                    showgrid= False,
                    showline= True,
                    linecolor= 'black',
                    linewidth= 2
                    )

    fig.update_layout(
                    title= {'text': 'Número de Animais Separados por Categorias',
                            'font': {'size': 15}}
    )

    return fig

def bar_doenca_resultado(df, resultado: str):
    """
    Função que retorna um gráfico com a quantidade de amostras com cada doença de interesse.

    Args:
        df: é o dataframe geral;
        resultado: tipo de resultado desejado para extrai a coluna 'inconclusivo', 'positivo' e 'negativo'.
    """
    
    df_resultado = pd.DataFrame({
        'Doença': ['Erliquiose', 'Babesiose', 'Anaplasmose', 'Leishmaniose', 'Cinomose'],
        'Contagem':[
                    len(df[df[f'{resultado}_doenca_interesse'].apply(lambda linha: 'Erliquiose' in linha)]),
                    len(df[df[f'{resultado}_doenca_interesse'].apply(lambda linha: 'Babesiose' in linha)]),
                    len(df[df[f'{resultado}_doenca_interesse'].apply(lambda linha: 'Anaplasmose' in linha)]),
                    len(df[df[f'{resultado}_doenca_interesse'].apply(lambda linha: 'Leishmaniose' in linha)]),
                    len(df[df[f'{resultado}_doenca_interesse'].apply(lambda linha: 'Cinomose' in linha)])
                    ]
    })

    fig = px.bar(
        data_frame= df_resultado.sort_values(by= 'Contagem', ascending= False),
        x= 'Doença',
        y= 'Contagem',
        color= 'Doença',
        color_discrete_map= {
            'Erliquiose': '#F0E442',
            'Babesiose': '#AB65B5',
            'Anaplasmose': '#679D50',
            'Leishmaniose': '#237AD5',
            'Cinomose': "#D52323" 
        },
        text_auto= True,
        width= 600,
        height= 400
    )

    fig.update_xaxes(
                    showgrid= False,
                    showline= True,
                    linewidth= 2,
                    linecolor= 'black'
                    )

    fig.update_yaxes(
                    showgrid= False,
                    showline= True,
                    linewidth= 2,
                    linecolor= 'black'
                    )

    fig.update_layout(
        title= {'text': f'Amostras com Diagnóstico {resultado} para Doenças de Interesse:',
                'font': {'size': 15}},
        showlegend= False
    )

    return fig