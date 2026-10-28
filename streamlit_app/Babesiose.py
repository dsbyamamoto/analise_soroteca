import sys
from pathlib import Path

# deixando o diretório analise_soroteca/ como raiz
raiz = Path(__file__).resolve().parent.parent
# verificando se essa raiz já foi adicionada. Caso não tenha sido, adicionar no sys.path
if str(raiz) not in sys.path:
    sys.path.insert(0, str(raiz))
    
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from graficos import bar_teste_rapido_doenca, bar_sorologia_doenca, pie_total_doentes, hist_idade, pie_sexo
from processamento import str_categorico, index_eppendorf_ID, diagnostico_suspeita_lista, diagnostico_tupla, tirar_duplicatas, ponto_de_corte
from filtros_info import df_doenca_total, sus_doenca, df_pcr_total, df_pcr_resultado, df_sexo_doenca, df_animais_estado, df_animais_municipio
from datetime import datetime

doenca_alvo= 'Babesiose'

st.set_page_config(
    page_title= doenca_alvo,
    page_icon= "🟣",
    layout= "wide"
)

st.sidebar.header("🟣:violet[Babesiose]")

# dados
df = pd.read_csv("dados/dados_tratados/soroteca_tratada1.csv")

# tratamento dos dados
df = str_categorico(df)
df = index_eppendorf_ID(df)
df = diagnostico_suspeita_lista(df)
df = diagnostico_tupla(df)
df = ponto_de_corte(df, 784)
df_semDuplicata = tirar_duplicatas(df)

# título da página 
st.title(f":violet[{doenca_alvo}]")

st.markdown(
    f"""
    Perfil de amostras diagnosticadas com **:violet[{doenca_alvo}]**    
    """
)

st.divider()

st.subheader(":grey-background[Visão Geral das Amostras]",
             text_alignment= 'center')

data_atual = datetime.now().strftime("%d/%m/%Y")
st.info(f'Estes dados estão atualizados até o dia: :red[31/06/2026] (data atual: {data_atual})', 
        icon="ℹ️",
        width= 700)

# filtrando amostras com Babesiose, tendo outros diagnósticos associados ou não
com_bab = len(df[df["diagnostico_final"].apply(lambda linha: doenca_alvo in linha)])
# percentual de amostras com Babesiose (c/ ou s/ outros diagnósticos) em relação ao número total de amostras
percentual_bab = round(len(df[df["diagnostico_final"].apply(lambda linha: doenca_alvo in linha)])/len(df) * 100, 2)
# filtrando amostras com suspeita ou resultados inconclusivos para Babesiose
sus_bab = sus_doenca(df, doenca= doenca_alvo, retorna_valor= 'sim')
# percentual de amostras inconclusivas para Babesiose em relação ao número total de amostras
percentual_sus_bab = round(sus_bab/len(df) * 100, 2)
# filtrando amostras apenas com Babesiose
apenas_bab = len(df[df['diagnostico_final'].apply(lambda linha: list(linha) == [doenca_alvo])])

bloco1, bloco2, bloco3 = st.columns(spec= [0.3, 0.3, 0.3],
                                    gap= 'small')
_, bloco4, bloco5, _ = st.columns([0.2, 0.3, 0.3, 0.2],
                                  gap= 'small')

with bloco1: 
    bloco1 = st.metric(
        label= 'Amostras com Babesiose:',
        value= f'{com_bab} de {len(df)} Amostras', 
        height= 'content',
        border= True,
        delta= f'{percentual_bab}%',
        delta_arrow= 'off',
        delta_color= 'violet'
    )
    st.caption(
        """
        OBS: vale salientar que :red[um mesmo animal pode possuir mais de uma amostra]. 
        Isso acontece, pois é também contabilizado as amostras de retorno. Neste caso,
        considera-se amostras que tenham Babesiose, independente se tem ou não outros
        diagnósticos associados. 
        """,
        text_alignment= 'justify'
    )

## número de animais únicos contabilizados (tirando duplicatas pelo código de identificação dos animais)
n_animais = df.drop_duplicates(subset= ['codigo_animal'], keep= 'first', inplace= False)
n_animais_bab = n_animais[n_animais['diagnostico_final'].apply(lambda linha: doenca_alvo in linha)]

with bloco2:
    bloco2 = st.metric(
        label= 'Nº de Cães c/ Babesiose (desconsidera retornos):',
        value= f'{len(n_animais_bab)} de {len(n_animais)} Animais',
        border= True,
        delta= f'{(len(n_animais_bab)/len(n_animais)) * 100:.2f}%',
        delta_color= 'violet',
        delta_arrow= 'off'
    )
    st.caption(
        """
        OBS: cada animal cadastrado possui um código interno de 5 dígitos para identificação própria. Este número representa
        o número de cães únicos, filtrando pelo código (desconsidera retornos) e que tenha Babesiose (com outros diagnósticos
        ou não).
        """,
        text_alignment= 'justify'
    )

with bloco3:
    bloco3 = st.metric(
        label= 'Amostras Inconclusivas para Babesiose:',
        value= f'{sus_bab} de {len(df)} Amostras',
        height= 'content',
        border= True,
        delta= f'{percentual_sus_bab}%',
        delta_color= 'violet',
        delta_arrow= 'off'
    )
    st.caption(
        """
        OBS: considera-se "Inconclusivo" para a doença de interesse, amostras que não possuem
        desfecho claro no prontuário, como nas seguintes situações: 
            **1. Suspeito para a doença-alvo, mas os testes não foram realizados**;
            **2. Feito os devidos testes, mas não foram atualizados no prontuário**;
            **3. Resultado de diagnóstico não muito confiável**.  
        """,
        text_alignment= 'justify'
    )

with bloco4:
    bloco4 = st.metric(
        label= f'Amostras c/ Babesiose + Outros Diagnósticos:',
        value= f'{com_bab - apenas_bab} de {com_bab} Amostras',
        border= True,
        delta= f'{round((com_bab - apenas_bab)/com_bab * 100, 2)}%',
        delta_arrow= 'off',
        delta_color= 'violet'
    )
    st.caption(
        """
        OBS: neste caso, considera-se apenas amostras que tenham Babesiose mais
        outro diagnóstico associado, excluindo amostras que tenham Babesiose como
        diagnóstico único, em relação ao nº de amostras totais c/ Babesiose (com ou
        sem outros diagnósticos associados). 
        """,
        text_alignment= 'justify'
    )

sexo_count = df_doenca_total(df, doenca= 'Babesiose')
sexo_count = sexo_count['sexo'].value_counts().reset_index().sort_values(by= ['count'], ascending= False)

with bloco5:
    bloco5 = st.metric(
        label= f'Há mais cães do gênero "{sexo_count.loc[0, 'sexo']}":',
        value= f'{int(sexo_count.loc[0, 'count'])} de {sexo_count['count'].sum()} Amostras',
        border= True,
        delta= f'{sexo_count.loc[0, 'count'] / sexo_count['count'].sum() * 100:.2f}%',
        delta_color= 'violet',
        delta_arrow= 'off'
    )
    st.caption(
        f"""
        OBS: Considerando todas as amostras c/ {doenca_alvo} (n = {sexo_count['count'].sum()}), temos mais cães {sexo_count.loc[0, 'sexo']}
        ({int(sexo_count.loc[0, 'count'])} -> {sexo_count.loc[0, 'count'] / sexo_count['count'].sum() * 100:.2f}%) 
        do que cães {sexo_count.loc[1, 'sexo']} ({int(sexo_count.loc[1, 'count'])} -> {sexo_count.loc[1, 'count'] / sexo_count['count'].sum() * 100:.2f}%).        
        """,
        text_alignment= 'justify'
    )

_, escolha1 = st.columns([0.5, 0.5],
                         gap= 'small')
gra1, gra2 = st.columns([0.5, 0.5],
                        gap = 'small')

with escolha1:
    escolha1 = st.selectbox('Perfil de Amostras c/ Babesiose, considerando o Sexo. Selecione uma Opção:',
                            ['Proporção de Gênero de Amostras c/ Babesiose', 'Distribuição de Amostras c/Babesiose considerando Faixa Etária']
                        )

# pie chart que vai mostrar a proporção de animais acometidos por babesiose em relação ao n total de animais
with gra1:
    fig1 = pie_total_doentes(df, doenca= doenca_alvo, cor_doenca= '#AB65B5', cor_total= '#5F6368')
    st.plotly_chart(fig1, width= 'content', height= 'content')
    st.caption(
        f"""
        **:primary-background[Fig 1.]** Pie chart que mostra a proporção de amostras afetadas por {doenca_alvo}
        em relação ao número total de amostras.
        """,
        text_alignment= 'justify'
    )

# histograma que vai mostrar a distribuição de cães com Babesiose pela idade
with gra2:
    if escolha1 == 'Proporção de Gênero de Amostras c/ Babesiose':
        fig2 = pie_sexo(df, doenca_alvo= doenca_alvo)
        st.plotly_chart(fig2, width= 'content', height= 'content')
        st.caption(
            f"""
            **:primary-background[Fig 2.]** Pie chart que mostra a proporção de machos e fêmeas que possuem {doenca_alvo}.
            Para isso, considera-se como referência o número de amostras com a doença, isso é, n = {com_bab}.
            """,
            text_alignment= 'justify'
        )
    elif escolha1 == 'Distribuição de Amostras c/Babesiose considerando Faixa Etária':
        fig3 = hist_idade(df, doenca= doenca_alvo)
        st.plotly_chart(fig3, width= 'content', height= 'content')
        st.caption(
            f"""
            **:primary-background[Fig 3.]** Histograma que mostra a distribuição de idade das amostras com {doenca_alvo}, 
            considerando também o sexo. IMPORTANTE: **:red[como o n amostral de animais com {doenca_alvo} é baixo, não é
            possível tirar conclusões precisas no momento]**. Pode ser que no futuro, com o aumento do número de amostras,
            seja possível tirar conclusões sobre. 
            """,
            text_alignment= 'justify'
        )

# RESUMO SOBRE LOCALIDADE 
escolha2, _ = st.columns([0.55, 0.45])

with escolha2:
    escolha2 = st.selectbox(
        f'Perfil de Amostras c/ {doenca_alvo}, considerando a Localização. Selecione uma Opção:',
        ['N° de Animais por Estado (Ordem Decrescente)', 'N° de Animais por Município (Ordem Decrescente)'] 
    )

gra3, blocos = st.columns([0.55, 0.45])

with gra3:
    if escolha2 == 'N° de Animais por Estado (Ordem Decrescente)':
        df1 = df_animais_estado(df, doenca= doenca_alvo)
        df1 = st.dataframe(
                    df1,
                    lazy= True
            )
        st.caption(
            f"""
            **:primary-background[DataFrame 1.]** Tabela que representa o número de amostras c/ Babesiose
            por Unidade Federativa. Considerou-se apenas os Estados que foram cadastrados durante o período
            de atualização da planilha, ou seja, Unidades Federativas que não tiveram pelo menos uma amostra
            contemplada, não foram consideradas.
            """,
            text_alignment= 'justify'
        )
    elif escolha2 == 'N° de Animais por Município (Ordem Decrescente)':
        df2 = df_animais_municipio(df, doenca= doenca_alvo) 
        df2 = st.dataframe(df2, lazy= True)
        st.caption(
            f"""
            **:primary-background[DataFrame 2.]** Tabela que representa o número de amostras c/ Babesiose
            por município. Considerou-se apenas os municípios que foram cadastrados durante o período
            de atualização da planilha, ou seja, municípios que não tiveram pelo menos uma amostra
            contemplada, não foram considerados.
            """,
            text_alignment= 'justify'
        ) 

with blocos:
    bloco6 = st.metric(
        label= 'Nº Total de Estados Contemplados (considerando as 27 UFs):',
        value= f'{len(df_animais_estado(df, doenca= doenca_alvo))} de 27 UFs',
        border= True,
        delta= f'{(len(df_animais_estado(df, doenca= doenca_alvo)) / 27) * 100:.2f}%',
        delta_color= 'violet',
        delta_arrow= 'off'
    )    
    bloco7 = st.metric(
        label= f'Nº Total de Municípios Contabilizados:',
        value= f'{len(df_animais_municipio(df, doenca= doenca_alvo))} Municípios',
        border= True
    )

    mun_mais_contagem = df_animais_municipio(df, doenca= doenca_alvo)

    bloco8 = st.metric(
        label= f'O Município com + amostras foi {mun_mais_contagem.loc[0]['Município']}-{mun_mais_contagem.loc[0]['Estado']} com:',
        value= f'{mun_mais_contagem.loc[0]['Contagem']} Amostras',
        border= True          
    )

st.divider()

st.subheader(":grey-background[Perfil de Testes p/ Diagnóstico]",
             text_alignment= 'center')

# gráfico que vai mostrar número de animais diagnosticados de acordo com o teste
_ ,escolha3, _, _ = st.columns([0.1, 0.55, 0.25, 0.1])
with escolha3:
    escolha3 = st.selectbox('Selecione qual o tipo do teste desejado:',
                            ('Teste Rápido', 'Sorologia'),
                        )       

_, gra4, bloco4, _ = st.columns([0.1, 0.55, 0.25, 0.1])

with gra4:
    if escolha3 == 'Teste Rápido':
        fig3 = bar_teste_rapido_doenca(df, eixo_x = 'babesiose_teste_rapido')
        st.plotly_chart(fig3)
        st.caption(
            f"""
            **:primary-background[Fig 3.]** Gráfico que representa o perfil de amostras testadas com uso de testes rápido
            para {doenca_alvo}. 
            """
        )
    elif escolha3 == 'Sorologia':
        fig4 = bar_sorologia_doenca(df, eixo_x = 'babesiose_ELISA')
        st.plotly_chart(fig4)
        st.caption(
            f"""
            **:primary-background[Fig 4.]** Gráfico que representa o perfil de amostras testadas por testes sorológicos para {doenca_alvo} 
            que especifiquem as imunoglobulinas testadas. IMPORTANTE: para resultado "(+) IgG e/ou (+) IgM", considera-se amostras
            que relatam positividade em teste sorológico, mas não dizem quais imunoglobulinas; para "(-) IgG e (-) IgM", amostras 
            com sorologia negativa.  
            """,
            text_alignment= 'justify'
        )
    st.caption(
        """
        OBS: É importante salientar que :red[uma mesma amostra pode ter sido testada
        por mais de um teste diferente] (exemplo: PCR + teste rápido)
        """,
        text_alignment= 'justify'
    )

with bloco4:
    bloco4 = st.metric(
        label= f'Amostras PCR + para {doenca_alvo}:',
        value= f'{len(df_pcr_resultado(df, eixo_x= "PCR_positivo", doenca= doenca_alvo))} de {len(df_pcr_total(df, doenca= doenca_alvo))}',
        width= 400,
        height= 'content',
        border= True,
        delta= f'{round(len(df_pcr_resultado(df, eixo_x= "PCR_positivo", doenca= doenca_alvo))/len(df_pcr_total(df, doenca= doenca_alvo)) * 100, 2)}%',
        delta_arrow= 'off',
        delta_color= 'violet'
    )

    bloco4 = st.metric(
        label= f'Amostras PCR - para {doenca_alvo}:',
        value= f'{len(df_pcr_resultado(df, eixo_x= "PCR_negativo", doenca= doenca_alvo))} de {len(df_pcr_total(df, doenca= doenca_alvo))}',
        width= 400,
        height= 'content',
        border= True,
        delta= f'{round(len(df_pcr_resultado(df, eixo_x= "PCR_negativo", doenca= doenca_alvo))/len(df_pcr_total(df, doenca= doenca_alvo)) * 100, 2)}%',
        delta_arrow= 'off',
        delta_color= 'violet'
    )

    bloco4 = st.metric(
        label= f'Amostras PCR Inconclusivo para {doenca_alvo}:',
        value= f'{len(df_pcr_resultado(df, eixo_x= "PCR_sem_resultado", doenca= doenca_alvo))} de {len(df_pcr_total(df, doenca= doenca_alvo))}',
        width= 350,
        height= 'content',
        border= True,
        delta= f'{round(len(df_pcr_resultado(df, eixo_x= "PCR_sem_resultado", doenca= doenca_alvo))/len(df_pcr_total(df, doenca= doenca_alvo)) * 100, 2)}%',
        delta_arrow= 'off',
        delta_color= 'violet'
    )
