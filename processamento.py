import pandas as pd

def tratamento_col(caminho_csv: str):
    """
    Função que irá apagar colunas não desejadas do meu DataFrame 

    Args:
        caminho_csv: PATH de onde o csv se encontra.
    """

    # importando o arquivo
    df = pd.read_csv(caminho_csv)
    
    # colunas_indesejadas com o nome de todas as colunas que são indesejáveis para a análise de dados
    colunas_indesejadas = [
                        'Identificação no eppendorf', 'Sangue total (assinalar com X)', 
                        'Soro (assinalar com X)', 'data da solicitação',
                          'idade ', 'peso (em kg)', 'endereços',
                        'UF_ref', 'municipio_ref', '23', '24', 'Volume Estimado da Amostra', 
                        'Concentração gDNA', 'Razão A260/280 gDNA', 'qPCR leish Feito?' 
                        ]
    
    # apagar as colunas indesejadas (inplace= False vai mudar o dataframe atual)
    df = df.drop(labels= colunas_indesejadas, axis= 1, inplace= False)
    
    return df

def index_eppendorf_ID(df):
    """
    Função que vai estabelecer a coluna "eppendorf_ID" como index 
    do dataframe

    Args:
        df: é o dataframe geral.
    """
    
    # vai configurar a coluna eppendorf_ID como novo indexador 
    df = df.set_index(keys= 'eppendorf_ID', inplace= False)

    return df

def codigo_animal_int(df):
    """
    Função que vai transformar o ID dos animais (código de 5 dígitos 
    estabelecidos pelo HV da UFV) do formato str para int. Além disso, 
    vai retirar linhas com códigos incongruentes 

    Args:
        df: é o dataframe geral.
    """
    
    # retirar a linha que tem um valor incongruente (linha 350 com código = 19,1 KG)
    df = df.drop(labels= 350, axis= 0, inplace= False)

    # trocando o tipo da coluna codigo_animal de str para Int64 (que aceita valores NA)
    df['codigo_animal'] = df['codigo_animal'].astype("Int64")

    return df

def str_categorico(df):
    """
    Função que vai pegar as colunas de str que contém categorias e transformar 
    em tipo category. Além disso, converterá a coluna "ano" de float para str

    Args:
        df: é o dataframe geral.
    """

    # listando todas as colunas que serão convertidas de str para category
    colunas_str = ['sangue', 'soro', 'formulario_coleta', 'termo_atendimento', 'mês', 'ano', 'sexo', 'raça', 'uf', 
                   'municipio', 'teve_leishmaniose', 'vacinado_leishmaniose', 'vacinado_leptospirose', 
                   'erliquiose_teste_rapido', 'babesiose_teste_rapido', 'anaplasmose_teste_rapido', 
                   'cinomose_teste_rapido', 'leishmaniose_teste_rapido', 'erliquiose_ELISA', 'babesiose_ELISA',
                   'anaplasmose_ELISA', 'leishmaniose_ELISA', 'PCR_positivo',
                   'PCR_negativo', 'PCR_sem_resultado'
                  ]

    # transformar a coluna 'ano' de float para str
    df['ano'] = df['ano'].astype("str")

    # convertendo str para category
    df[colunas_str] = df[colunas_str].astype("category")

    return df

def tirar_na(df):
    """
    Função que irá tirar linhas que tenham valor nulo nas colunas: 'codigo_animal', 
    'termo atendimento' e 'diagnostico_final'

    Args:
        df: é o dataframe geral.
    """

    # definindo colunas que não podem ter valores NA
    colunas_sensiveis = ['codigo_animal', 'termo_atendimento', 'diagnostico_final']

    # remove as linhas que tenham valores NA nas colunas_sensiveis
    df = df.dropna(subset= colunas_sensiveis, axis= 0, inplace= False)

    return df

def termo_presente(df):
    """
    Função que vai desconsiderar linhas que não tenham o termo de atendimento

    Args:
        df: é o dataframe geral.
    """

    # dataframe que considera apenas animais que tenham termo de atendimento
    df = df[df['termo_atendimento'] == 'Sim']

    return df

def diagnostico_suspeita_lista(df):
    """
    Função que vai transformar os valores das colunas "diagnostico_final",
    "teve_hemoparasitose", "inconclusivo_doenca_interesse", "positivo_doenca_interesse" e
    "negativo_doenca_interesse" (colunas que podem receber múltiplos valores) em listas 

    Args:
        df: é o dataframe geral.
    """

    # vai separar cada elemento e transformar tudo em uma lista de str
    # Com exceção de 'diagnostico_final', todas as outras colunas aceitam valores nulos. As linhas com valores nulos retornam listas vazias
    df['diagnostico_final'] = df['diagnostico_final'].str.split(", ")
    df['teve_hemoparasitoses'] = df['teve_hemoparasitoses'].apply(lambda linha: [] if pd.isna(linha) else linha.split(", "))
    df['inconclusivo_doenca_interesse'] = df['inconclusivo_doenca_interesse'].apply(lambda linha: [] if pd.isna(linha) else linha.split(", "))
    df['positivo_doenca_interesse'] = df['positivo_doenca_interesse'].apply(lambda linha: [] if pd.isna(linha) else linha.split(", "))
    df['negativo_doenca_interesse'] = df['negativo_doenca_interesse'].apply(lambda linha: [] if pd.isna(linha) else linha.split(", "))
 
    return df 

def diagnostico_tupla(df):
    """
    Função que transforma as listas em tuplas ordenadas
    
    - Motivo: transformando em tuplas ordenadas, não importa a ordem preenchida, 
    pois os diferentes arranjos serão considerados como uma mesma categoria.

    Args:
        df: é o dataframe geral.   
    """

    # transformando as colunas com formato de lista em tuplas (importante, pois a ordem do preenchimento não importa)
    df['diagnostico_final'] = df['diagnostico_final'].apply(lambda linha: tuple(sorted(linha)))
    df['teve_hemoparasitoses'] = df['teve_hemoparasitoses'].apply(lambda linha: tuple(sorted(linha)))
    df['inconclusivo_doenca_interesse'] = df['inconclusivo_doenca_interesse'].apply(lambda linha: tuple(sorted(linha)))
    df['positivo_doenca_interesse'] = df['positivo_doenca_interesse'].apply(lambda linha: tuple(sorted(linha)))
    df['negativo_doenca_interesse'] = df['negativo_doenca_interesse'].apply(lambda linha: tuple(sorted(linha)))

    return df

def tirar_duplicatas(df):
    """
    Função que vai retirar duplicatas de animais com o mesmo código e diagnóstico

    Args:
        df: é o dataframe geral.
    """

    # vai retirar duplicatas mantendo a primeira ocorrência
    df = df.drop_duplicates(subset= ['codigo_animal', 'diagnostico_final'], keep='first', inplace= False)

    return df

def formatar_str(df, coluna= str):
    """
    Função que irá formatar as strings no csv, tirando os espaços vazios

    Args:
        df: é o dataframe geral;
        coluna: coluna da planilha que vai formatar as strings. 
    """

    # retirando espaços vazios nas categorias da coluna dada como argumento
    df[coluna] = df[coluna].str.strip()

    return df

def ponto_de_corte(df, id_corte: int):
    """
    Função em que define um id como ponto de corte

    Args:
        df: é o dataframe geral;
        id_corte: id que define o ponto de corte.
    """

    df = df.loc[1:id_corte]

    return df

def dataframe_tratado(caminho_csv: str):
    """
    Função que vai executar todas as funções de tratamento e salvar o DataFrame final 
    no diretório dados_tratados

    Args:
        caminho_csv: PATH de onde o arquivo da soroteca está localizado.
    """
    
    # execução de todas as funções de processamento
    df_tratado = tratamento_col(caminho_csv)
    df_tratado = index_eppendorf_ID(df_tratado)
    df_tratado = codigo_animal_int(df_tratado)
    df_tratado = formatar_str(df_tratado, coluna= 'raça')
    df_tratado = termo_presente(df_tratado)
    df_tratado = tirar_na(df_tratado)

    # nomeando arquivo tratado
    arquivo_csv = caminho_csv.split('/')[-1]
    arquivo_tratado = arquivo_csv.replace('soroteca', 'soroteca_tratada')

    # salvar o dataframe tratado no diretório dados_tratados
    df_tratado = df_tratado.to_csv(f"dados/dados_tratados/{arquivo_tratado}")
    print("Processamento concluido com sucesso. Arquivo final salvo em: /dados/dados_tratados/")
