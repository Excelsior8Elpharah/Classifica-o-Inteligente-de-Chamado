# 🧠 Pipeline Inteligente de Machine Learning para Classificação de Chamados

A HelpNow, startup especializada em soluções inteligentes para atendimento ao cliente, enfrenta diariamente um alto volume de chamados recebidos, o que gera atrasos no tempo de resposta e dificulta a priorização de demandas críticas. Para resolver esse problema, foi desenvolvido um pipeline completo de Machine Learning com foco na classificação automática de chamados por nível de urgência — Alta, Média ou Baixa — com base no conteúdo textual e em dados tabulares.

O projeto foi construído com uma abordagem de ponta a ponta, passando por geração e análise exploratória de dados, limpeza e pré-processamento de texto, vetorização com TF-IDF, engenharia de features, treinamento e avaliação de modelos supervisionados, e simulação de deployment. Foram testados diferentes algoritmos de aprendizado supervisionado, incluindo Random Forest, XGBoost, SVM, com o objetivo de identificar a melhor performance em termos de precisão e F1-Score ponderado.

A solução foi desenvolvida em Google Colab, utilizando ferramentas modernas como Pandas, NumPy, Scikit-learn, TensorFlow/Keras e XGBoost TensorFlow/Keras, garantindo reprodutibilidade e escalabilidade. Além disso, foi implementada uma função de predição simulando o comportamento de uma API em produção, permitindo que novos chamados sejam classificados automaticamente em tempo real.

Com isso, a HelpNow poderá reduzir o tempo médio de atendimento, priorizar casos críticos de forma automatizada e aumentar a eficiência operacional, melhorando significativamente a experiência do cliente.

---

## ⚙️ Etapas Principais do Projeto

### 1. Configuração do Ambiente

* Instalação e importação de bibliotecas essenciais: `pandas`, `numpy`, `scikit-learn`, `xgboost`, `torch`, `tensorflow` e `imbalanced-learn`.
* Criação de uma base sólida para manipulação de dados, modelagem, balanceamento e deep learning.

### 2. Geração e Carregamento de Dados

* Uso da biblioteca **Faker** para gerar dados sintéticos realistas quando não há dataset real disponível.
* Campos simulados: `dias_atraso`, `valor_divida`, `texto_chamado` e `urgência`.
* Regras de negócio coerentes para garantir um *target* válido.

### 3. Análise Exploratória (EDA)

* Estatísticas descritivas, correlação e visualizações (heatmaps, boxplots, barplots).
* Confirmação da relação lógica entre atraso, dívida e urgência.

### 4. Pré-processamento e Limpeza de Texto

* Normalização textual: minúsculas, remoção de pontuação e *stopwords*.
* Preparação dos dados para vetorização via **TF-IDF**.

### 5. Codificação e Desbalanceamento

* Transformação da variável *urgência* em valores numéricos.
* Análise de distribuição de classes e justificativa para uso de métricas ponderadas e `class_weight='balanced'`.

### 6. Vetorização e Engenharia de Features

* Vetorização do texto com **TF-IDF** (unigramas e bigramas).
* Combinação de features textuais e tabulares em uma única matriz.

### 7. Treinamento e Avaliação de Modelos

Modelos comparados:

* 🌲 Random Forest
* 🚀 XGBoost
* 🧠 SVM
* 🤖 Rede Neural (Keras/TensorFlow)

Métrica principal: **F1-Score Ponderado**.

> **Resultado:** Random Forest apresentou melhor equilíbrio entre desempenho e interpretabilidade.

### 8. Diagnóstico e Interpretabilidade

* Análise de falsos negativos, vetores de suporte e curvas de perda.
* Entendimento das fronteiras de decisão e comportamento dos modelos.

### 9. Deployment Simulado

* Serialização dos artefatos: modelo, scaler, vetorizador e codificador.
* Função `priorizar_chamado()` simulando uma API em produção:

  * Entrada: texto e dados tabulares de um chamado.
  * Saída: prioridade (`Alta`, `Média`, `Baixa`).

### 10. Integração com BI e Revalidação

* Preparação para integração futura com dashboards e sistemas de monitoramento.
* Garantia de **reprodutibilidade**, **confiabilidade** e **escalabilidade**.

---

## 🚀 Conclusão

Este projeto demonstra o ciclo completo de um **sistema inteligente de priorização de chamados** — unindo:

* 🧪 Ciência de Dados
* 🤖 Machine Learning
* 🧰 Boas práticas de Engenharia de Software

Com ele, empresas podem transformar dados textuais e operacionais em **decisões automatizadas e baseadas em evidências**, otimizando o tempo de resposta e a eficiência no atendimento ao cliente.

---

## 🧾 Stack Tecnológica

* **Linguagem:** Python
* **Bibliotecas principais:** `pandas`, `numpy`, `scikit-learn`, `xgboost`, `torch`, `tensorflow`, `faker`, `matplotlib`, `seaborn`
* **Modelos:** Random Forest, XGBoost, SVM, Rede Neural
* **NLP:** TF-IDF Vectorizer
* **Métrica de Avaliação:** F1-Score Ponderado
* **Simulação de Deployment:** API de predição com função `priorizar_chamado()`
