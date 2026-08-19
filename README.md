# NASA Asteroid Data Analysis

> Projeto acadêmico desenvolvido na **FATEC Sebrae**, no curso de **Ciência de Dados para Negócios**, com foco em **Análise Exploratória de Dados (EDA)** e visualização interativa.

## Sobre o projeto

A proposta da atividade era selecionar uma base de dados, independentemente do tema, e aplicar técnicas de análise exploratória para compreender suas características, identificar padrões e comunicar os resultados por meio de diferentes visualizações.

Para este projeto, foi escolhida uma base de dados relacionada a **asteroides**, obtida no Kaggle, contendo informações como classe orbital, diâmetro, magnitude absoluta, período orbital, excentricidade, albedo, MOID e classificação como potencialmente perigoso (PHA).

A partir dessa base, foi desenvolvido um dashboard interativo utilizando **Python e Streamlit**, com o objetivo de explorar os dados de diferentes perspectivas e transformar os resultados da análise em informações visuais e interpretáveis.

## Objetivos

* Realizar uma análise exploratória da base de dados de asteroides.
* Trabalhar tratamento e preparação dos dados utilizando Python.
* Explorar diferentes variáveis e suas relações.
* Utilizar diferentes tipos de gráficos para comunicar os resultados.
* Desenvolver uma aplicação interativa com Streamlit.
* Criar indicadores e insights a partir dos dados filtrados.

## Dashboard

O dashboard permite explorar a base de forma interativa por meio de filtros e visualizações.

Entre os filtros disponíveis estão:

* Classe orbital;
* Classificação PHA;
* Faixa de diâmetro;
* Magnitude absoluta (H).

Os filtros modificam dinamicamente os dados utilizados nas análises e nos indicadores apresentados.

### Indicadores

O dashboard apresenta indicadores gerais sobre a seleção atual, incluindo:

* Total de asteroides;
* Percentual de objetos classificados como PHA;
* Percentual com MOID inferior a 0,05 AU;
* Percentual com período orbital inferior a 2 anos;
* Percentual de asteroides com diâmetro superior a 1 km.

### Visualizações

Foram utilizadas diferentes técnicas de visualização para explorar a base, entre elas:

* Gráficos de barras para comparação de percentuais;
* Gráfico de rosca para distribuição por classe orbital;
* Distribuição dos asteroides por tamanho;
* Scatter plot entre MOID e diâmetro;
* Scatter plot entre magnitude absoluta e diâmetro;
* Box plot para análise da excentricidade orbital por classe.

A utilização de diferentes gráficos foi parte importante do objetivo da atividade, permitindo observar os mesmos dados sob diferentes perspectivas.

## Insights

Além das visualizações, o dashboard possui uma seção de **Insights Automáticos**, responsável por transformar alguns resultados estatísticos da seleção atual em informações textuais.

Entre os indicadores analisados estão:

* Proporção de asteroides potencialmente perigosos;
* Proximidade em relação à Terra através do MOID;
* Classe orbital predominante;
* Proporção de objetos com mais de 1 km;
* Mediana da magnitude absoluta;
* Percentual de diâmetros estimados;
* Proporção de objetos com período orbital inferior a 2 anos.

Dessa forma, o projeto busca ir além da apresentação dos gráficos, utilizando os resultados obtidos para facilitar a interpretação da base.

## Tecnologias utilizadas

| Tecnologia | Utilização                             |
| ---------- | -------------------------------------- |
| Python     | Desenvolvimento da análise e aplicação |
| Pandas     | Manipulação e tratamento dos dados     |
| Plotly     | Criação das visualizações interativas  |
| Streamlit  | Desenvolvimento do dashboard           |
| CSV        | Armazenamento da base de dados         |

## Estrutura principal

```text
Project_Nasa_Fatec/
│
├── Dashboard.py
├── asteroides.csv
├── asteroides_perigosos_novo.py
├── index.html
└── LICENSE
```

O arquivo `Dashboard.py` concentra a aplicação principal de análise exploratória, incluindo carregamento e tratamento da base, filtros, indicadores, visualizações e geração dos insights.

## Aplicação

O projeto possui uma versão publicada para demonstração:

**[Acessar aplicação](https://project-nasa-fatec.vercel.app)**

## Contexto acadêmico

Este projeto foi desenvolvido como parte das atividades da **FATEC Sebrae — Ciência de Dados para Negócios**.

A atividade teve como foco a aplicação prática dos conceitos de **análise exploratória de dados e visualização**, permitindo trabalhar desde a escolha e preparação da base até a construção de uma aplicação capaz de apresentar os resultados de forma interativa.

Mais do que analisar especificamente asteroides, o projeto representa a aplicação de um processo de exploração de dados utilizando Python e ferramentas de visualização.

---

**Desenvolvido por Darlan Henricon**
Ciência de Dados para Negócios — FATEC Sebrae
