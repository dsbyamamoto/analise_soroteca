import pandas as pd
from processamento import tirar_duplicatas

# Informações 
def sus_doenca(df, doenca: str, retorna_valor= 'não'):
    """
    Função que vai retornar o número ou gera uma descrição em texto das amostras 
    que precisam ser testadas para uma determinada doença-alvo

    Args:
    - df: é o dataframe geral (PRECISA JÁ TER PASSADO POR diagnostico_tupla() );
    - doenca: doença de interesse entre "Erliquiose", "Babesiose", "Anaplasmose", 
               "Leishmaniose", "Cinomose" e "Leptospirose";
    - retorna_valor: retorna uma descrição se retorna_valor= 'não' ou retorna o 
                      valor len(df) se retorna_valor= 'sim'.
    
    Returns:
        int: retorna o tamanho do dataframe filtrado se 'retorna_valor' == 'sim'.
    """

    # filtrando as amostras que tenham 'Inconclusivo' no diagnóstico final e que tenham algo preenchido em 'inconclusivo_doenca_interesse'
    suspeita_df = df[df['diagnostico_final'].apply(lambda linha: 'Inconclusivo' in linha)]
    # filtra apenas os valores não vazios (retira linhas com tuplas vazias). Atenção: os valores de 'inconclusivo_doenca_interesse' precisam já estar formatados em tuplas!  
    suspeita_df = suspeita_df[~(suspeita_df['inconclusivo_doenca_interesse'] == ())] 

    # filtro de animais com diagnóstico inconclusivo e que tenham suspeita para alguma doença de interesse (declarada pelo parâmetro 'doenca')
    suspeita_df = suspeita_df[(suspeita_df["inconclusivo_doenca_interesse"].apply(lambda linha: doenca in linha)) & (suspeita_df["diagnostico_final"].apply(lambda linha: 'Inconclusivo' in linha))]

    if retorna_valor == 'não':
        # Retorna uma descrição da consulta, de acordo com a doença escolhida
        print(f"Número de animais com suspeita para {doenca} e que precisam ser testados: {len(suspeita_df)}")
    elif retorna_valor == 'sim':
        # Retorna apenas o número de amostras que precisam ser testadas para a determinada doença
        return len(suspeita_df)

def teste_rapido(df, doenca: str, resultado: str):
    teste_rapido = df[f'{doenca}_teste_rapido'].value_counts().to_dict()
    if resultado == 'Positivo':
        return teste_rapido.get('Positivo', 0)
    elif resultado == 'Negativo':
        return teste_rapido.get('Negativo', 0)
    else:
        return teste_rapido.get('Sem Resultado', 0)

def teste_elisa(df, doenca: str, resultado: str):
    teste_elisa = df[f'{doenca}_ELISA'].value_counts().to_dict()
    if resultado == '(+) IgG':
        return teste_elisa.get('(+) IgG', 0)
    elif resultado == '(+) IgM':
        return teste_elisa.get('(+) IgM', 0)
    elif resultado == '(+) IgG e (+) IgM':
        return teste_elisa.get('(+) IgG e (+) IgM', 0)
    elif resultado == '(+) IgG e/ou (+) IgM':
            return teste_elisa.get('(+) IgG e/ou (+) IgM', 0)
    elif resultado == '(-) IgG e (-) IgM':
            return teste_elisa.get('(-) IgG e (-) IgM', 0)
    else:
        return teste_elisa.get('Sem Resultado', 0)

def numero_diagnostico(df, doenca: str, sexo= None, raca= None):
    """
    Função que vai retornar o número de animais diagnosticados de acordo com os argumentos dados
    como filtros.

    Args:
        df: é o dataframe geral;
        doenca: qualquer categoria de diagnóstico utilizada no preenchimento da planilha;
        sexo: filtro por sexo ('Macho' ou 'Fêmea');
        raca: filtro por raça presente na planilha.
    """

    if sexo is not None and raca is None:
        # retorna o número de animais diagnosticados pela doença-alvo de acordo com o sexo
        return len(df[(df['diagnostico_final'].apply(lambda linha: doenca in linha)) & (df['sexo'] == sexo)])
    elif sexo is None and raca is not None:
        # retorna o número de animais diagnosticados pela doença-alvo de acordo com a raça
        return len(df[(df['diagnostico_final'].apply(lambda linha: doenca in linha)) & (df['raça'] == raca)])
    elif sexo is None and raca is None:
        # retorna o número de animais diagnosticados pela doença-alvo, independentemente do sexo e raça
        return len(df[df['diagnostico_final'].apply(lambda linha: doenca in linha)])

# DataFrames 
def df_pcr_total(df, doenca: str):
    """
    Função que vai retornar o DataFrame de amostras que fizeram PCR com todos os resultados
    e de acordo com a doença de interesse 

    Args:
        df: é o dataframe geral;
        doenca: doença de interesse entre "Erliquiose", "Babesiose", "Anaplasmose", 
                "Leishmaniose" e "Cinomose".
    Returns:
        dataframe: retorna um dataframe com todas as amostras submetidas ao PCR.
    """

    pcr_feito = df[(df['PCR_positivo'] == doenca) | (df['PCR_negativo'] == doenca) | (df['PCR_sem_resultado'] == doenca)]

    return pcr_feito

def df_pcr_resultado(df, eixo_x: str, doenca: str):
    """
    Função que vai retornar o DataFrame de amostras de PCR de acordo com eixo_x (resultado) 
    e a doença-alvo.

    Args:
        df = é o dataframe geral;
        eixo_x = é a coluna de PCR: PCR_positivo, PCR_negativo, PCR_sem_resultado;
        doenca = doença de interesse entre "Erliquiose", "Babesiose", "Anaplasmose", 
                 "Leishmaniose" e "Cinomose".
    
    Returns:
        dataframe: retorna o dataframe filtrado de acordo com o resultado e doença escolhidos.
    """

    resultado_pcr = df[df[eixo_x] == doenca]

    return resultado_pcr

def df_doenca_total(df, doenca: str, duplicata= 'sim', modo= 'dataframe'):
    """
    Função que vai dar o número total de acometidos pelo parâmetro 'doenca', tendo outros 
    diagnósticos ou não. Avalia também se as duplicatas são ou não consideradas.
    
    Args:
        df: dataframe contendo os dados.
        doenca: qualquer categoria de doença no formato da planilha (ex: 'Leishmaniose');
        duplicata: se considera ou não as duplicatas (aceita "sim" ou "não"). 
                   Default = 'sim';
        modo: retorna uma descrição (modo= 'descrito') ou o dataframe (modo= 'dataframe'). 
              Default = 'dataframe'.
    
    Returns:
        str: retorna descrição do número de acometidos, se modo= 'descrito';
        dataframe: retorna dataframe dos acometidos pela doença-alvo, se modo= 'dataframe'. 
    """

    # fatiando as colunas de interesse para a saída do dataframe
    df = df[['codigo_animal', 'sexo', 'idade_aproximada_anos', 'mês', 'ano','uf', 'municipio', 
             'Suspeita clínica/diagnóstico', 'Diagnóstico Final (Prontuário)',
             'diagnostico_final']]
    # filtrando os animais que tenham a doença, considerando também outros diagnósticos associados
    df = df[df['diagnostico_final'].apply(lambda linha: doenca in linha)]

    if duplicata == 'sim':
        if modo == 'descrito':
            # número de linhas que tenha a doença, considerando também outros diagnósticos (com duplicatas)
            print(f"Número de animais com {doenca}, considerando outros diagnósticos (c/ duplicatas): {len(df)}")
        elif modo == 'dataframe':
            return df 
        else:
            print('Erro na função! Provavelmente o erro reside no parâmetro: modo (aceita "descrito" ou "dataframe")') 
    elif duplicata == 'não':
        # tirando as duplicatas e mantendo a primeira ocorrência de cães que tenham a doença (incluindo outros diagnósticos)
        df = tirar_duplicatas(df)
        if modo == 'descrito':
            # número de linhas que tenha a doença, considerando também outros diagnósticos (sem duplicatas) 
            print(f'Número de animais com {doenca}, considerando outros diagnósticos (s/ duplicatas): {len(df)}')
        elif modo == 'dataframe':
            return df
        else:
            print('Erro na função! Provavelmente o erro reside no parâmetro: modo (aceita "descrito" ou "dataframe")') 
    else:
        print('Erro na função! Provavelmente o erro reside no parâmetro: duplicata (aceita "sim" ou "não")')

def df_apenas_doencas(df, doenca: str, duplicata= 'sim', modo= 'dataframe'):
    """
    Função que vai dar o número total de acometidos por doença-alvo, desconsiderando 
    outros diagnósticos que podem estar associados. Avalia também se as duplicatas são
    ou não consideradas.
    
    Args:
        df: dataframe contendo os dados;
        doenca: qualquer categoria de doença no formato da planilha (ex: 'Leishmaniose');
        duplicata: se considera ou não as duplicatas (aceita "sim" ou "não").
                   Default = 'sim';
        modo: retorna uma descrição (modo= 'descrito') ou o dataframe (modo= 'dataframe').
              Default = 'dataframe'.
    
    Returns:
        str: retorna descrição do número de acometidos, se modo= 'descrito';
        dataframe: retorna dataframe dos acometidos pela doença-alvo, se modo= 'dataframe'.
    """

    # fatiando as colunas de interesse para a saída do dataframe
    df = df[['codigo_animal','idade_aproximada_anos', 'mês', 'ano','uf', 'municipio', 
             'Suspeita clínica/diagnóstico', 'Diagnóstico Final (Prontuário)',
             'diagnostico_final']]

    # filtrando todos os cães que tem a doença, desconsiderando outros diagnósticos
    df = df[df['diagnostico_final'].apply(lambda linha: list(linha) == [doenca])]
    
    if duplicata == 'sim':
        if modo == 'descrito':
            # número de linhas que tenha a doença, desconsiderando outros diagnósticos (com duplicatas)
            print(f"Número de animais com {doenca}, desconsiderando outros diagnósticos (c/ duplicatas): {len(df)}")
        elif modo == 'dataframe':
            return df 
        else:
            print('Erro na função! Provavelmente o erro reside no parâmetro: modo (aceita "descrito" ou "dataframe")') 
    elif duplicata == 'não':
        # tirando as duplicatas e mantendo a primeira ocorrência de cães que tenham a doença 
        df = tirar_duplicatas(df)
        if modo == 'descrito':
            # número de linhas que tenha a doença, desconsiderando outros diagnósticos (sem duplicatas)
            print(f'Número de animais com {doenca}, desconsiderando outros diagnósticos (s/ duplicatas): {len(df)}')
        elif modo == 'dataframe':
            return df
        else:
            print('Erro na função! Provavelmente o erro reside no parâmetro: modo (aceita "descrito" ou "dataframe")') 
    else:
        print('Erro na função! Provavelmente o erro reside no parâmetro: duplicata (aceita "sim" ou "não")')

# CONTROLE INTERNO
def avaliar_duplicata_doenca(df, doenca: str):
    """
    Função que retorna as linhas com as duplicatas e suas
    respectivas descrições

    Args:
        df: dataframe contendo os dados;
        doenca: qualquer categoria de doença no formato da planilha (ex: 'Leishmaniose').
    """

    # usando a função doencas_total para pegar todos os animais que tenham a doença
    df = df_doenca_total(df, doenca)

    # filtrando apenas as duplicatas
    df = df[df.duplicated(subset= ['codigo_animal', 'diagnostico_final'], keep= False)]

    print(f'Duplicatas de animais diagnosticados com {doenca}')

    # iterando linha por linha e retornando as informações das duplicatas
    df = df.sort_values(by = 'codigo_animal')
    for i, linha in df.iterrows():
        print(f"{i} código: {linha['codigo_animal']} -> {linha['Diagnóstico Final (Prontuário)']}")

def df_animais_municipio(df, doenca = None):
    """
    Função que retorna um DataFrame com os municípios com mais amostras contabilizadas.
    Apenas os municípios que tiveram casos cadastrados foram considerados. Ainda é possível
    filtrar as contagens com base na doença-alvo dada como argumento

    Args:
        df: dataframe contendo os dados;
        doenca: qualquer categoria de doença no formato da planilha (ex: 'Leishmaniose').
    """

    df['municipio'] = df['municipio'].str.strip()
    if doenca is None:
        df = df[(df['uf'].notnull()) & (df['municipio'].notnull())]
    else:
        df = df[(df['uf'].notnull()) & (df['municipio'].notnull()) & (df['diagnostico_final'].apply(lambda linha: doenca in linha))]
    
    df = df[['uf', 'municipio']]
    df = df.groupby(by= ['municipio', 'uf']).size().reset_index(name= 'Contagem').sort_values(by = 'Contagem', ascending= False)
    df = df.reset_index().drop(labels= 'index', axis= 1).rename(columns= {'municipio': 'Município', 'uf': 'Estado'})

    return df

def df_animais_estado(df, doenca = None):
    """
    Função que retorna um DataFrame com o número de amostras por Unidade Federativa. 
    Apenas os Estados que tiveram casos foram considerados. Ainda é possível filtrar
    estas contagens com base na doença-alvo dada como argumento

    Args:
        df: dataframe contendo os dados;
        doenca: qualquer categoria de doença no formato da planilha (ex: 'Leishmaniose').
    """

    df = df[['uf', 'diagnostico_final']]
    if doenca is not None:
        df = df[df['diagnostico_final'].apply(lambda linha: doenca in linha)]
    
    df = df['uf'].dropna().reset_index()
    df = df.drop(labels = 'eppendorf_ID', axis= 1)
    df = df.groupby(by = ['uf']).size().reset_index(name= 'Contagem').sort_values(by= 'Contagem', ascending= False)
    df = df.reset_index().drop(labels= 'index', axis= 1).rename(columns= {'uf': 'Estado'})

    return df

def df_contagem_geral(df):
    """
    Função que retorna um DataFrame com a contagem de acometidos por cada categoria 
    de diagnóstico considerada na elaboração da planilha

    Args:
        df: é o dataframe geral.
    """

    df = pd.DataFrame([
        {"Doença": 'Tumor', "Quantidade": numero_diagnostico(df, 'Tumor')},
        {"Doença": 'Erliquiose', "Quantidade": numero_diagnostico(df, 'Erliquiose')},      
        {"Doença": 'Babesiose', "Quantidade": numero_diagnostico(df, 'Babesiose')},
        {"Doença": 'Leishmaniose', "Quantidade": numero_diagnostico(df, 'Leishmaniose')},
        {"Doença": 'Leptospirose', "Quantidade": numero_diagnostico(df, 'Leptospirose')},
        {"Doença": 'Cinomose', "Quantidade": numero_diagnostico(df, 'Cinomose')},
        {"Doença": 'Anaplasmose', "Quantidade": numero_diagnostico(df, 'Anaplasmose')},
        {"Doença": 'Doença de Chagas', "Quantidade": numero_diagnostico(df, 'Doença de Chagas')},
        {"Doença": 'Otite', "Quantidade":  numero_diagnostico(df, 'Otite')},
        {"Doença": 'Doença urológica/renal', "Quantidade":  numero_diagnostico(df, 'Doença urológica/renal')}, 
        {"Doença": 'Doença dermatológica', "Quantidade":  numero_diagnostico(df, 'Doença dermatológica')},
        {"Doença": 'Doença odontológica', "Quantidade":  numero_diagnostico(df, 'Doença odontológica')},
        {"Doença": 'Doença ocular', "Quantidade":  numero_diagnostico(df, 'Doença ocular')},
        {"Doença": 'Doença respiratória', "Quantidade":  numero_diagnostico(df, 'Doença respiratória')},
        {"Doença": 'Doença periodontal', "Quantidade":  numero_diagnostico(df, 'Doença periodontal')},
        {"Doença": 'Doença endócrina', "Quantidade":  numero_diagnostico(df, 'Doença endócrina')},
        {"Doença": 'Doença reprodutiva', "Quantidade":  numero_diagnostico(df, 'Doença reprodutiva')},
        {"Doença": 'Doença gastrointestinal', "Quantidade":  numero_diagnostico(df, 'Doença gastrointestinal')},
        {"Doença": 'Doença cardiovascular', "Quantidade":  numero_diagnostico(df, 'Doença cardiovascular')},
        {"Doença": 'Doença musculoesquelética', "Quantidade":  numero_diagnostico(df, 'Doença musculoesquelética')},
        {"Doença": 'Outros', "Quantidade":  numero_diagnostico(df, 'Outros')},
        {"Doença": 'Inconclusivo', "Quantidade":  numero_diagnostico(df, 'Inconclusivo')},
        {"Doença": 'Doença neurológica', "Quantidade":  numero_diagnostico(df, 'Doença neurológica')}
    ]).sort_values(by= 'Quantidade', ascending= True)

    return df

def df_combinacoes_doenca(df):
    """
    Função que retorna um DataFrame com todas as combinações de diagnósticos
    do DataFrame base e suas respectivas contagens.

    Args:
        df: é o dataframe geral.
    """

    df_diag = df['diagnostico_final'].value_counts()
    df_diag = pd.DataFrame(df_diag).reset_index().rename(columns= {'diagnostico_final': 'Combinações de Diagnósticos', 'count': 'Contagem'})

    return df_diag

# Retorna o DataFrame Completo com todas as combinações com pelo menos uma doença de interesse
def df_doencas_interesse(df):
    """
    Função que retorna um DataFrame com combinações que tenham pelo menos
    uma doença de interesse.

    Args:
        df: é o dataframe geral
    """

    df = df_combinacoes_doenca(df)
    doencas_interesse = df[df['Combinações de Diagnósticos'].apply(lambda linha: 
                                                               'Erliquiose' in linha or 
                                                               'Anaplasmose' in linha or 
                                                               'Leishmaniose' in linha or
                                                               'Cinomose' in linha or
                                                               'Babesiose' in linha
                                                               )
                            ]
    
    return doencas_interesse

# Retorna um DataFrame com as coinfecções associadas à doença de interesse dada como argumento 
def df_coinf_doenca(df, doenca= str):
    """
    Função que retorna um DataFrame com os animais com a doença-alvo mais
    outra doença de interesse associada.

    Args:
        df: é o dataframe geral;
        doenca: doença de interesse entre "Erliquiose", "Babesiose", "Anaplasmose", "Leishmaniose" e "Cinomose".
    """

    coinfec = df[(df['positivo_doenca_interesse'].apply(lambda linha: doenca in linha)) & 
                 (~df['positivo_doenca_interesse'].apply(lambda linha: list(linha) == [doenca]))
                 ]
    coinfec = coinfec['positivo_doenca_interesse'].value_counts().reset_index()
    coinfec = coinfec.rename(columns= {'positivo_doenca_interesse': 'Combinações', 'count': 'Contagem'})

    return coinfec

def df_sexo_doenca(df, doenca: str, sexo= 'Fêmea'):
    """
    Função que retorna um Dataframe com as amostras acometidas pela doença escolhida,
    filtrando pelo gênero desejado.

    Args:
        df: é o dataframe geral;
        doenca: qualquer doença presente na planilha base;
        sexo: filtra por gênero ('Macho' e 'Fêmea'). Default = 'Fêmea'.
    """
    if sexo == 'Fêmea':
        femea = df[
                    (df['sexo'] == 'Fêmea') & 
                    (df['diagnostico_final'].apply(lambda linha: doenca in linha))
                ]

        return femea
    
    elif sexo == 'Macho':
        macho = df[
                    (df['sexo'] == 'Macho') &
                    (df['diagnostico_final'].apply(lambda linha: doenca in linha))
                ]   

        return macho