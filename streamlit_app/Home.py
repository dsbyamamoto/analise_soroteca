import streamlit as st

st.set_page_config(
    page_title= "Página Inicial",
    page_icon= "🏠",
    layout= "wide"
)

st.sidebar.header("🏠 Página Inicial")

st.title("Dashboard - Soroteca UFV")

st.markdown(
    """
    ### Sobre 📋
    Este é um dashboard interativo feito para resumir os dados de uma planilha
    elaborada pelo **Laboratório de Infectologia Animal (LIMA)** do Departamento de
    Bioquímica da Universidade Federal de Viçosa (UFV) sobre amostras de sangue e soro
    de cães obtidos pelo Laboratório Clínico do Departamento de Veterinária da mesma 
    instituição.

    Esta parceria com o departamento de veterinária resultou na elaboração de uma 
    planilha, cujo objetivo em comum é avaliar o perfil de doenças em cães de interesse
    mútuo entre os departamentos. Entre as doenças de interesse, tem-se:
    
    - Leishmaniose
    - Cinomose
    - Erliquiose
    - Babesiose
    - Anaplasmose

    Com estes dados, é possível mapear e analisar as amostras obtidas pelo Laboratório Clínico
    Veterinário, sendo possível extrair informações sobre o perfil dos animais atendidos no 
    Hospital de Pequenos Animais da UFV, além de servir como fonte de dados para pesquisas e projetos
    no Laboratório de Infectologia Animal (LIMA) ou outros interessados.
    """,
    text_alignment= 'justify'
)

st.divider()

st.markdown(
    """
    ### Integridade dos Dados ⚠️
    Por questões éticas, **:red[nenhum dos dados dispostos neste dashboard faz referência ao nome ou
    qualquer informação que permita a identificação do animal]**, sendo apenas um resumo geral dos dados
    obtidos. 

    O acesso a planilha não é permitido e não será divulgado para o público geral, uma vez que contém informações sensíveis sobre tutores e seus
    respectivos animais. Estes dados estão disponibilizados apenas para os condutores da pesquisa, professores
    responsáveis e estagiários inseridos no projeto. Para que cada amostra seja cadastrada, tem que haver consentimento prévio
    do uso dessas amostras pelos(as) próprios(as) preceptores(as) mediante a assinatura do **termo de atendimento** e **formulário de coleta**, 
    documentos em que o(a) responsável permite o uso de excedentes de amostras para fins de pesquisa e coleta informações sanitárias do animal, respectivamente
    """,
    text_alignment= 'justify'
)