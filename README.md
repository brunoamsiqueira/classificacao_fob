# App: Assistente de Classificação do Fator de Obsolescência do Imóvel

## Contexto

As prefeituras geralmente possuem uma área de **Apoio Técnico** vinculada ao setor de cadastro imobiliário, responsável por realizar análises técnicas. Essas análises são baseadas em **decretos municipais e na Planta Genérica de Valores (PGV)**.

Essas equipes costumam ser formadas por profissionais de diferentes áreas da engenharia e técnicos especializados em **geoprocessamento e análise territorial**.

Apesar da importância dessas atividades, muitas administrações municipais ainda enfrentam **defasagem tecnológica nos processos de análise cadastral**, o que reduz a velocidade das avaliações e mantém parte significativa das decisões baseada em interpretações subjetivas dos avaliadores.

Diante desse cenário, este projeto teve como objetivo **desenvolver um assistente digital para classificação do fator de obsolescência de imóveis**, padronizando a coleta de dados e automatizando o processo de classificação.

---

# Problema

A classificação do **Fator de Obsolescência** apresenta alto grau de subjetividade, pois depende da interpretação individual de cada avaliador.

O método tradicional utiliza descrições genéricas, como *“bom”, “regular” ou “ruim”*, para avaliar o estado do imóvel como um todo. Essa abordagem gera diversos problemas:

* Inconsistência entre laudos técnicos quando analisado por analistas distintos;
* Dificuldade de padronização entre avaliadores;
* Limitação na análise territorial baseada em dados cadastrais.

Sem um método estruturado de avaliação, a classificação final pode variar significativamente entre profissionais, mesmo diante de condições construtivas semelhantes.

---

# Modelo de avaliação e solução proposta

O fator de obsolescência é um indice que faz parte do calculo do valor venal do imóvel.

Para reduzir a subjetividade desse processo, foi desenvolvido um **Assistente Virtual de Classificação de Obsolescência**.

O funcionamento ocorre da seguinte forma:

1. O analista avalia **09 elementos construtivos** do imóvel (estrutura, cobertura, esquadrias, instalações, acabamentos etc.).
2. Para cada item, o sistema apresenta **opções padronizadas de estado de conservação**.
3. O assistente calcula automaticamente uma **nota técnica ponderada (0 a 100)**.
4. Com base nessa nota, o sistema retorna o **enquadramento técnico do fator de obsolescência**, conforme os parâmetros estabelecidos no decreto municipal que são: Ótimo; Muito Bom; Bom; Intermediário; Regular; Deficiente; Ruim; e Muito Ruim.

Dessa forma, o processo passa a ter:

* Padronização na coleta de dados;
* Redução da subjetividade;
* Maior consistência entre avaliações;
* Possibilidade de integração com sistemas de geoprocessamento municipal.

---

# Metodologias aplicadas

Para padronizar a classificação do fator de correção de obsolescência, foi desenvolvido um modelo baseado em **Árvore de Decisão Multicritério**, implementado por meio de um **Assistente Virtual de Vistoria Técnica**.

## 1. Matriz de Ponderação Construtiva

A avaliação do imóvel foi estruturada a partir da decomposição da edificação em **09 elementos construtivos principais**, cada um com peso proporcional à sua relevância estrutural.

Os elementos avaliados são:

* Estrutura
* Cobertura
* Acabamento interno
* Acabamento externo
* Instalações elétricas
* Instalações hidráulicas
* Pisos
* Forro
* Idade real aparente da edificação

Cada elemento recebe uma **pontuação baseada em seu estado de conservação**, seguindo níveis padronizados definidos no modelo de avaliação.

A classificação final é obtida por meio de uma **média ponderada das notas atribuídas aos elementos construtivos**, conforme a fórmula:

```
Nota Final Ponderada = Σ(Nota × Peso) / Σ(Pesos)
```

Esse modelo permite transformar uma avaliação qualitativa em um **indicador quantitativo padronizado**, reduzindo inconsistências entre avaliadores.

---

## 2. Sistema de Pontuação

Cada elemento construtivo possui **opções pré-definidas de estado de conservação**, associadas a notas que variam em um intervalo de **1 a 8**.

Durante a vistoria, o analista apenas seleciona a condição física observada para cada item. O sistema então calcula automaticamente a média ponderada e determina a classificação final do fator de obsolescência.

Esse processo elimina cálculos manuais e reduz o risco de erros na avaliação.

---

## 3. Tecnologia utilizada

A ferramenta foi desenvolvida por meio de um **script em Python**, permitindo que o assistente seja utilizado tanto em **dispositivos móveis (vistoria de campo)** quanto em **computadores utilizados pela equipe técnica**.

Esse modelo possibilita:

* Uso individual por cada analista
* Execução local sem necessidade de softwares complexos
* Fácil adaptação para integração futura com sistemas de cadastro técnico ou geoprocessamento municipal

---

## Estrutura de ponderação dos elementos construtivos

| Elemento                | Peso (%) |
| ----------------------- | -------- |
| Estrutura               | 25       |
| Cobertura               | 20       |
| Acabamento Interno      | 12       |
| Acabamento Externo      | 12       |
| Instalações Elétricas   | 7        |
| Instalações Hidráulicas | 7        |
| Pisos                   | 7        |
| Forro                   | 5        |
| Idade Real Aproximada   | 5        |
