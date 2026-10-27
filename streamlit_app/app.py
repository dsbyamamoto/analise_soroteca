import streamlit as st

# carregando todas as páginas
home_page = st.Page("Home.py", icon= "🏠", title= 'Página Inicial')
geral_page = st.Page("visao_geral.py", icon= "🔎", title= 'Dashboard Geral')
erl_page = st.Page("Erliquiose.py", icon= "🟡")
bab_page = st.Page("Babesiose.py", icon= "🟣")
leish_page = st.Page("Leishmaniose.py", icon= "🔵")
anap_page = st.Page("Anaplasmose.py", icon= "🟢")
cin_page = st.Page("Cinomose.py", icon= "🔴")

pg = st.navigation([home_page, geral_page, erl_page, bab_page, leish_page, anap_page, cin_page])
pg.run()
