# Análise de Soroteca: Perfil de Amostras de Cães do Laboratório Clínico Veterinário UFV

## Descrição Breve do Projeto 
<div align= "justify">

Projeto autônomo desenvolvido durante o período de estágio obrigatório do curso de Medicina Veterinária da Universidade Federal de Viçosa (UFV), sob orientação da Profª Juliana Fietto[^1] do Laboratório de Infectologia Molecular Animal (LIMA). Consiste na **análise dos dados de uma soroteca com amostras de sangue e soro de cães obtidos no Laboratório Clínico Veterinário do Departamento de Veterinária da UFV**, durante os períodos de Julho de 2024 à Junho de 2026, para o desenvolvimento de pesquisas tanto para o Departamento de Veterinária, quanto para outros parceiros/interessados (ex: equipe da professora Juliana que necessita de dados de cães com Leishmaniose para pesquisa interna).
</div>

## Principais Objetivos
<div align= "justify">

Entre os principais objetivos pessoais com esse projeto, tinham-se:
- Tirar insights sobre os dados da planilha; 
- Auxiliar doutorandos e interessados, de acordo com suas demandas;
- Avaliar o perfil diagnóstico das amostras, sobretudo para algumas doenças de interesse para a equipe do estágio;
    - Doenças de Interesse: **Leishmaniose**, **Erliquiose**, **Babesiose**, **Anaplasmose** e **Cinomose** (dados usados para avaliação epidemiológica e pesquisa interna);
- Aprendizado próprio, aplicando análise de dados em contexto real na medicina veterinária.
</div>

## Sobre os Dados e Ética
<div align= "justify">

Os dados são oriundos da rotina do Laboratório Clínico Veterinário, do Departamento Veterinário da UFV. As amostras de soro e sangue de cães atendidos pelo Hospital Veterinário de Pequenos Animais da UFV são encaminhadas para o laboratório clínico e, assim, criou-se uma rotina para pegar estas amostras e registrá-las em uma planilha. **Esta planilha, por questões de privacidade e ética, não será disponibilizada neste repositório**, sendo disposto apenas o arquivo em CSV com dados sensíveis ocultados ou modificados.
</div>

> [!IMPORTANT]
> Por questão de ética, todas as amostras cadastradas na planilha e posteriormente utilizadas para estudos foram averiguadas, quanto a assinatura de termo e formulário de coleta. Estes documentos atestam que o(a) tutor(a) responsável permite o uso de excedentes das amostras para fins de estudo e pesquisa. Além disso, informações que possam, de alguma forma, permitir o rastreamento ou identificação do animal foram ocultadas (exemplo: nome e código de atendimento associado ao animal).   

## Principais Resultados
<div align= "justify">

Com base nessas análises, tem-se como principais resultados:

- **70 das 643 amostras contabilizadas (10.89%) possuem pelo menos uma das doenças de interesse (Leishmaniose, Erliquiose, Babesiose, Anaplasmose e Cinomose) como diagnóstico final**;
- Entre as doenças de interesse, **Erliquiose** e **Babesiose** são as que mais possuem amostras diagnosticadas: 41 (6.38%) e 36 (5.60%) amostras, respectivamente;
- **57** das 258 amostras inconclusivas (22.09%) são inconclusivas para alguma doença de interesse;
- O diagnóstico destas amostras com doença de interesse foi realizado, majoritariamente, por testes rápidos e sorologias. **Diagnóstico molecular (PCR) foi feito em apenas 10 amostras**, tendo como diagnóstico positivo 3 para Leishmaniose, 1 para Erliquiose e 1 para Cinomose. Isso indica que o padrão-ouro é pouco utilizado para diagnosticar estas doenças, sendo muitas vezes os testes sorológicos utilizados como base para conduta clínica;
- Desconsiderando a categoria de "Inconclusivo", **Tumor com 139 das 643 amostras (21.62%)** foi o diagnóstico com maior número de amostras.
</div>

## Como Reproduzir?
### Requisitos
<div align= "justify">

- Git instalado no computador
- Possuir algum gerenciador de ambientes/pacotes (recomendado: conda)
- Python 3.14.7
- Baixar as libs do requirements.txt
</div>

### Passo-a-passo
<div align= "justify">

1. Clonar o projeto do repositório virtual para o local
2. Para rodar o projeto, basta digitar no terminal streamlit run streamlit_app/app.py
</div>

<div align= "justify">

[^1]: Professora titular e pesquisadora do Departamento de Bioquímica da UFV. Atua na área de Biotecnologia e Bioquímica, com ênfase em biologia molecular, produção de proteínas recombinantese e aplicações biotecnológicas, bioquímica de enzimas e biologia celular, voltados para doenças infecciosas humanas e animais. Para mais detalhes, consultar currículo [Lattes](http://lattes.cnpq.br/2782262776744934) 
</div>
