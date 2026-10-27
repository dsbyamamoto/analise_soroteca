import sys
from pathlib import Path

# deixando o diretório analise_soroteca/ como raiz
raiz = Path(__file__).resolve().parent.parent
# verificando se essa raiz já foi adicionada para localizar os módulos fora de streamlit_app/ 
if str(raiz) not in sys.path:
    # Caso não tenha sido, adicionar na primeira posição de sys.path para agilizar a procura
    sys.path.insert(0, str(raiz))

import streamlit as st 
import pandas as pd
from graficos import hist_idade, pie_sexo, bar_animais_raca, bar_geral, bar_geral_sexo, bar_doenca_resultado
from processamento import str_categorico, index_eppendorf_ID, diagnostico_suspeita_lista, diagnostico_tupla, tirar_duplicatas, ponto_de_corte
from filtros_info import df_animais_municipio, df_animais_estado, df_contagem_geral, df_combinacoes_doenca, df_doencas_interesse
from datetime import datetime

st.set_page_config(
    page_title= "Dashboard Geral",
    page_icon= "🔎",
    layout= "wide"
)

st.sidebar.header("🔎 Dashboard Geral")

# dados
df = pd.read_csv("dados/dados_tratados/soroteca_tratada1.csv")

# tratamento dos dados
df = str_categorico(df)
df = index_eppendorf_ID(df)
df = diagnostico_suspeita_lista(df)
df = diagnostico_tupla(df)
df = ponto_de_corte(df, 784)
df_semDuplicata = tirar_duplicatas(df)

st.title("Dashboard Geral")

st.markdown(
    """
    As amostras utilizadas foram obtidas no período de **:primary-background[Junho de 2024 a Junho de 2026]**, totalizando dois anos de coleta. É importante salientar que
    nesse intervalo houve períodos em que a coleta foi interrompida por questões de logística e de equipe. A **capacitação de pessoas** acompanhada de **mudanças constantes na equipe** e **padronização
    dos procedimentos** foram os principais fatores que dificultaram a dinâmica de atualização destes dados.
    """,
    text_alignment= 'justify'
)

st.divider()

st.subheader(":grey-background[Visão Geral das Amostras]",
             text_alignment= 'center')

data_atual= datetime.now().strftime("%d/%m/%Y")
st.info(f'Estes dados estão atualizados até o dia: :red[31/06/2026] (data atual: {data_atual})', 
        icon="ℹ️",
        width= 700)

# informações gerais das amostras -------------------------------------------------------------------------------------
bloco1, bloco2, bloco3 = st.columns(spec= [0.3, 0.3, 0.3], 
                                    gap= 'small')

with bloco1:
    bloco1.metric(
        label= 'Total de Amostras Contabilizadas:',
        value= f'{len(df)} Amostras',
        width= 500, 
        height= 130,
        border= True,
    )
    st.caption(
        """
        OBS: vale salientar que :red[um mesmo animal pode possuir mais de uma amostra]. 
        Isso acontece, pois é também contabilizado as amostras de retorno
        """,
        text_alignment= 'justify'
    )

## número de animais únicos contabilizados (tirando duplicatas pelo código de identificação dos animais)
n_animais = df.drop_duplicates(subset= ['codigo_animal'], keep= 'first', inplace= False)

with bloco2:
    bloco2.metric(
        label= 'Número de Cães (sem considerar os retornos):',
        value= f'{len(n_animais)} de {len(df)} Animais',
        width= 600,
        height= 130,
        border= True,
        delta= f'{round((len(n_animais) / len(df)) * 100, 2)}%',
        delta_color= 'grey',
        delta_arrow= 'off'
    )
    st.caption(
        """
        OBS: cada animal cadastrado possui um código interno de 5 dígitos para identificação própria. Este número representa
        o número de cães únicos, filtrando pelo código (desconsidera retornos)
        """,
        text_alignment= 'justify'
    )

sexo_count = df['sexo'].value_counts().sort_values(ascending= False)

with bloco3:
    bloco3.metric(
        label= f'Há mais cães do gênero "{sexo_count.index[0]}":',
        value= f'{int(sexo_count.iloc[0])} de {len(df)} Amostras',
        width= 600,
        height= 130,
        border= True,
        delta= f'{sexo_count.iloc[0] / len(df) * 100:.2f}%',
        delta_color= 'grey',
        delta_arrow= 'off'
    )
    st.caption(
        f"""
        OBS: Considerando todas as amostras (n = {len(df)}), temos mais cães {sexo_count.index[0]} ({int(sexo_count.iloc[0])} 
        -> {sexo_count.iloc[0] / len(df) * 100:.2f}%) do que cães {sexo_count.index[1]} ({int(sexo_count.iloc[1])} 
        -> {sexo_count.iloc[1] / len(df) * 100:.2f}%).        
        """,
        text_alignment= 'justify'
    )

st.warning(
    f'Para as demais análises, foi considerado o :red[número total de amostras contabilizadas], \
    isso é, considerando todos os retornos de um mesmo animal (n = {len(df)} amostras)', 
    icon="⚠️"
    )
# ---------------------------------------------------------------------------------------------------------------------------

escolha1, escolha2 = st.columns([0.5, 0.5])

with escolha1:
    escolha1 = st.selectbox(
        'Perfil das Amostras em relação ao Sexo. Selecione uma Opção:',
        ('Proporção', 'Distribuição considerando Faixa Etária'),
    )

with escolha2:
    escolha2 = st.selectbox(
        'Perfil de Raças. Selecione uma Opção:',
        ('Visão Geral dos Grupos de Raça', 'Raças c/ respectivas Contagens e Grupamentos'),
    )

grade1, grade2 = st.columns([0.5, 0.5])

with grade1:
    if escolha1 == 'Proporção':
        fig1 = pie_sexo(df)
        st.plotly_chart(fig1, width= 'content', height= 'content')
        st.caption(
            """
            **:primary-background[Fig 1.]** Pie Chart que mostra o percentual de amostras de cães fêmeas e machos.
            Obs: ao passar o mouse por cima, é possível ver o número absoluto de cada gênero.
            """,
            text_alignment= 'justify'
        )
    elif escolha1 == 'Distribuição considerando Faixa Etária':
        fig2 = hist_idade(df)
        st.plotly_chart(fig2, width= 'content', height= 'content')
        st.caption(
            """
            **:primary-background[Fig 2.]** Histograma que mostra a distribuição de amostras contabilizadas por faixa etária
            e segmentado por sexo. Além disso, há um boxplot integrado que fornece informações dos quartis,
            mediana e possíveis outliers. 
            Obs: é possível filtrar os dados pelo sexo. Basta clicar na caixa da legenda para ocultar a informação
            de uma categoria (ex: para ver a distribuição de machos, basta clicar na caixa de fêmeas).
            """,
            text_alignment= 'justify'
        )

with grade2:
    if escolha2 == 'Visão Geral dos Grupos de Raça':
        fig3 = bar_animais_raca(df)
        st.plotly_chart(fig3, width= 'content', height= 'content')
        st.caption(
            """
            **:primary-background[Fig 3.]** Gráfico de barras que mostra o número de animais por grupo de raça.
            Obs: Estes agrupamentos podem sofrer alterações, pois ainda é preciso rever se as 
            categorias e seus constituintes estão alocados de forma adequada.
            """,
            text_alignment= 'justify'
        )
    elif escolha2 == 'Raças c/ respectivas Contagens e Grupamentos':
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

        df1 = df['raça'].dropna()
        df1 = df1.value_counts()
        df1 = pd.DataFrame(df1)
        df1 = df1.reset_index()
        df1 = df1.rename(columns= {'raça': 'Raça', 'count': 'Contagem'})
        df1['Grupos'] = df1['Raça'].map(grupo_raca)
        st.dataframe(df1, lazy= True)
        st.caption(
            """
            **:primary-background[DataFrame 1.]** Tabela que retorna as raças registradas com o Grupo que foi considerado
            e o número de animais por categoria. Obs: **:yellow[Estes agrupamentos podem sofrer alterações, 
            pois ainda é preciso rever se as categorias e seus constituintes estão alocados de forma adequada]**.
            """,
            text_alignment= 'justify'
        )

escolha3, _ = st.columns([0.55, 0.45])

with escolha3:
    escolha3 = st.selectbox(
        "Perfil de Amostras, considerando Localização. Selecione uma Opção:",
        ['N° de Animais por Estado (Ordem Decrescente)', 'N° de Animais por Município (Ordem Decrescente)']
    )

grade3, blocos = st.columns([0.55, 0.45])

with grade3:
    if escolha3 == 'N° de Animais por Estado (Ordem Decrescente)':
        df2 = df_animais_estado(df)
        st.dataframe(df2, lazy= True)
        st.caption(
            """
            **:primary-background[DataFrame 2.]** Tabela que retrata as Unidades Federativas com suas respectivas
            contagens de amostras. Considerou-se apenas os Estados que foram cadastrados durante o período
            de atualização da planilha, ou seja, Unidades Federativas que não tiveram pelo menos uma amostra
            contemplada, não foram consideradas.
            """,
            text_alignment= 'justify'
        )
    elif escolha3 == 'N° de Animais por Município (Ordem Decrescente)':
        df3 = df_animais_municipio(df)
        st.dataframe(df3, lazy= True)
        st.caption(
            """
            **:primary-background[DataFrame 3.]** Tabela que retrata os municípios contabilizados com suas respectivas
            contagens de amostras e Unidade Federativa correspondente. Considerou-se apenas os municípios 
            que foram cadastrados durante o período de atualização da planilha, ou seja, municípios que não 
            tiveram pelo menos uma amostra contemplada, não foram considerados.
            """,
            text_alignment= 'justify'
        )

with blocos:
    bloco4 = st.metric(
        label= f'Nº Total de Estados Contemplados (considerando as 27 UFs):',
        value= f'{len(df_animais_estado(df))} de 27 UFs',
        width= 500,
        height= 130,
        border= True,
        delta= f'{len(df_animais_estado(df)) / 27 * 100:.2f}%',
        delta_color= 'grey',
        delta_arrow= 'off'
    )

    bloco5 = st.metric(
        label= f'Nº Total de Municípios Contabilizados:',
        value= f'{len(df_animais_municipio(df))} Municípios',
        width= 500,
        height= 130,
        border= True
    )

    mun_mais_contagem = df_animais_municipio(df)

    bloco6 = st.metric(
        label= f'O Município com + amostras foi {mun_mais_contagem.loc[0]['Município']}-{mun_mais_contagem.loc[0]['Estado']} com:',
        value= f'{mun_mais_contagem.loc[0]['Contagem']} Amostras',
        width= 500,
        height= 130,
        border= True          
    )

st.divider()

# PERFIL DE DIAGNÓSTICOS

st.subheader(":grey-background[Perfil Diagnóstico]",
             text_alignment= 'center')

st.markdown(
    """
    Para facilitar a análise dos dados, as diferentes doenças foram agrupadas em categorias 
    :gray[(Exemplo: diabetes mellitus e hiperadrenocorticismo foram agrupados em "Doenças Endócrinas")]. \n
    - Doenças de Interesse: Erliquiose, Babesiose, Anaplasmose, Leishmaniose e Cinomose.
    """
)

st.warning(
    """
    **:red[Informações Importantes]** \n
    - Um mesmo animal pode ter uma ou mais categorias de diagnósticos associados
    - "Inconclusivo" pode significar ausência de informação sobre o desfecho clínico ou de resultados de exames para qualquer diagnóstico 
    :gray[(Exemplo: um mesmo animal pode ter Doença Dermatológica, mas a descrição do prontuário ficou Inconclusivo para Babesiose)]
    """,
    icon= "⚠️"
)

bloco7, bloco8, bloco9 = st.columns([0.35, 0.35, 0.3],
                                    gap= 'small')

# bloco7: indica a categoria de diagnóstico mais frequente (desconsiderando "Inconclusivo") e sua respectiva contagem
with bloco7:
    df_geral = df_contagem_geral(df)
    if df_geral.loc[0, 'Doença'] == 'Inconclusivo':
        doenca_mais_frequente = df_geral.loc[1, 'Doença']
        quantidade_mais_frequente = df_geral.loc[1, 'Quantidade']
    else:
        doenca_mais_frequente = df_geral.loc[0, 'Doença'] 
        quantidade_mais_frequente = df_geral.loc[0, 'Quantidade']
    bloco7 = st.metric(
        label= 'Categoria com + Amostras (Exceto "Inconclusivo"):',
        value= f'{doenca_mais_frequente} ({quantidade_mais_frequente} amostras)',
        border= True,
        height= 'content'
    )
    st.caption(
        """
        OBS: esta informação considera amostras que tenham mais de uma categoria de diagnóstico
        associadas (referência "Fig 4."). Dessa forma, não se pode comparar este valor com 
        o total de amostras do estudo, uma vez que uma mesma amostra pode estar contemplada
        em mais de uma categoria de diagnóstico. 
        """,
        text_alignment= 'justify'
    )

with bloco8:
    bloco8 = st.metric(
        label= 'Nº de Amostras c/ pelo menos uma Doença de Interesse:',
        value= f'{df_doencas_interesse(df)['Contagem'].sum()} de {len(df)} Amostras',
        border= True,
        height= 'content',
        delta= f'{df_doencas_interesse(df)['Contagem'].sum() / len(df) * 100:.2f}%',
        delta_color= 'grey',
        delta_arrow= 'off'
    )
    st.caption(
        """
        OBS: este valor não é a soma simples dos diagnósticos descritos na "Fig 4.", uma vez que a contagem 
        desse gráfico é pela nº de ocorrências (exemplo: um animal com Erliquiose e Babesiose, a contagem
        vai considerar 1 Erliquiose e 1 Babesiose). Neste caso em específico, o **:yellow[somatório considera amostras
        que tenham pelo menos uma doença de interesse]** (utilizando o exemplo anterior, conta como
        uma amostra na contagem).
        """,
        text_alignment= 'justify'
    )

with bloco9:
    # filtrando o número de amostras com doença de interesse
    df_resultado = pd.DataFrame({
        'Doença': ['Erliquiose', 'Babesiose', 'Anaplasmose', 'Leishmaniose', 'Cinomose'],
        'Contagem':[
                    len(df[df['positivo_doenca_interesse'].apply(lambda linha: 'Erliquiose' in linha)]),
                    len(df[df['positivo_doenca_interesse'].apply(lambda linha: 'Babesiose' in linha)]),
                    len(df[df['positivo_doenca_interesse'].apply(lambda linha: 'Anaplasmose' in linha)]),
                    len(df[df['positivo_doenca_interesse'].apply(lambda linha: 'Leishmaniose' in linha)]),
                    len(df[df['positivo_doenca_interesse'].apply(lambda linha: 'Cinomose' in linha)])
                    ]
    }).sort_values(by= 'Contagem', ascending= False) 
    bloco9 = st.metric(
        label= f'Doença de Interesse com + Amostras -> **{df_resultado.loc[0, 'Doença']}**',
        value= f'{df_resultado.loc[0, "Contagem"]} Amostras',
        border= True,
        height= 'content',
        delta= f'{df_resultado.loc[0, "Contagem"] / int(df_resultado["Contagem"].sum()) * 100:.2f}% de {int(df_resultado["Contagem"].sum())} amostras',
        delta_color= 'grey',
        delta_arrow= 'off'
    )
    st.caption(
       f"""
        OBS: considera a soma simples de cada categoria, isso é, contabiliza todas as doenças de interesse
        de cada amostra, mesmo uma mesma amostra tendo mais de uma. O valor de {int(df_resultado["Contagem"].sum())}
        amostras representa o somatório de todas as doenças de interesse, diferente do valor de {df_doencas_interesse(df)['Contagem'].sum()},
        que inclui no somatório todas as amostras que possuem pelo menos uma doença de interesse (Referência: "Fig 6.").
        """,
        text_alignment= 'justify'
    )

escolha4 = st.selectbox(
        "Perfil de Diagnósticos. Selecione uma opção:",
        ['Nº de Amostras por Diagnóstico', 'Nº de Amostras por Diagnóstico (Considerando o Sexo)'],
        width= 'stretch'
)


if escolha4 == 'Nº de Amostras por Diagnóstico':
    fig4 = bar_geral(df)
    st.plotly_chart(fig4, width= 'content', height= 'content')
    st.caption(
        """
        **:primary-background[Fig 4.]** Gráfico que retrata a quantidade de amostras por categoria de diagnóstico. 
        OBS: as colunas destacadas em vermelho representam as doenças de interesse.
        """,
        text_alignment= 'justify'
    )
elif escolha4 == 'Nº de Amostras por Diagnóstico (Considerando o Sexo)':
    fig5 = bar_geral_sexo(df)
    st.plotly_chart(fig5, width= 'content', height= 'content')
    st.caption(
        """
        **:primary-background[Fig 5.]** Gráfico que retrata a quantidade de amostras por categoria de diagnóstico, considerando o sexo. 
        """,
        text_alignment= 'justify'
    )

_, escolha5 = st.columns([0.6, 0.4])

with escolha5:
    escolha5 = st.selectbox(
        "Perfil de Diagnóstico por Doença de Interesse (Somatório de cada Categoria). Selecione uma Opção:",
        ["Amostras com Resultado (+) para Doenças de Interesse", "Amostras com Resultado (-) para Doenças de Interesse"]
    )

grade4, grade5 = st.columns([0.6, 0.4])

with grade4: 
    st.write("Contagem de Amostras por Combinação de Diagnósticos:")
    df4 = df_combinacoes_doenca(df)
    st.dataframe(df4, lazy= True)
    st.caption(
        """
        **:primary-background[DataFrame 4.]** Tabela com as diferentes combinações de diagnósticos por categoria e suas respectivas frequências 
        """,
        text_alignment= 'justify'
    )

with grade5:
    if escolha5 == 'Amostras com Resultado (+) para Doenças de Interesse':
        fig6 = bar_doenca_resultado(df, resultado= 'positivo')
        st.plotly_chart(fig6, width= 'content', height= 'content')
        st.caption(
            """
            **:primary-background[Fig 6.]** Número de animais com diagnóstico positivo (+) para as doenças de interesse, 
            independente do teste realizado. OBS: Para mais informações sobre os resultados por teste, navegue pela página 
            específica da doença de interesse.
            """,
            text_alignment= 'justify'
        )
    elif escolha5 == 'Amostras com Resultado (-) para Doenças de Interesse':
        fig7 = bar_doenca_resultado(df, resultado= 'negativo')
        st.plotly_chart(fig7, width= 'content', height= 'content')
        st.caption(
            """
            **:primary-background[Fig 7.]** Número de animais com diagnóstico negativo (-) para as doenças de interesse, 
            independente do teste realizado. OBS: Para mais informações sobre os resultados por teste, navegue pela página  
            específica da doença de interesse
            """,
            text_alignment= 'justify'
        )



    